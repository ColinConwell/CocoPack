import os, io, re, shutil
import bibtexparser # 1.x

from copy import copy
from glob import glob
from pathlib import Path
from PIL import Image
from tqdm.auto import tqdm
from datetime import datetime

# Initial Setup -----------------------------------------------------------

def set_overleaf_root(overleaf_root=None):
    global OVERLEAF_ROOT
    if overleaf_root is not None:
        OVERLEAF_ROOT = overleaf_root
        
    else: # prompt user for root
        OVERLEAF_ROOT = input('Enter the Overleaf root directory: ')
    
def _check_overleaf_root_oninit():
    overleaf_root_found = False

    if 'OVERLEAF_ROOT' in globals():
        overleaf_root_found = True

    if 'OVERLEAF_ROOT' in os.environ:
        overleaf_root_found = True

    return overleaf_root_found

def _check_bibtexparser_version():
    return bibtexparser.__version__.startswith('1')

if not _check_bibtexparser_version():
    raise ImportError("bibtexparser1.x, To fix, try:",
                      "\npip install bibtexparser~=1.0")

if not _check_overleaf_root_oninit():
    set_overleaf_root() # set root directory

# Core Functions ----------------------------------------------------------

def get_overleaf_root(overleaf_root=None):
    if overleaf_root is None: # fetch from globals
        if 'OVERLEAF_ROOT' in globals():
            return globals().get('OVERLEAF_ROOT')

        if 'OVERLEAF_ROOT' in os.environ:
            return os.environ.get('OVERLEAF_ROOT')
            
        else: # raise error if root not in globals
            raise ValueError('Overleaf root not specified.')
    
    return overleaf_root

def get_overleaf_path(project_name, overleaf_root=None):
    overleaf_root = get_overleaf_root(overleaf_root)
    return os.path.join(overleaf_root, project_name)

def get_overleaf_projects(overleaf_root=None, exclusions=[], sort_by_date=True, **kwargs):
    overleaf_root = get_overleaf_root(overleaf_root) # fetch root
    
    overleaf_paths = [(os.path.getmtime(path), path) for path
                      in glob(os.path.join(overleaf_root, '*'))]
    
    project_list = [(date, os.path.basename(path)) for date, path 
                    in overleaf_paths if os.path.isdir(path)]
    
    if exclusions is not None and len(exclusions) > 0:
        project_list = [(date, project) for date, project in project_list 
                        if not any([ex in project for ex in exclusions])]
            
    if sort_by_date: # return projects in order of modification:
        project_list = sorted(project_list, reverse=True)
        
        if kwargs.pop('verbose', False):
            for date, project in project_list:
                date = (datetime.fromtimestamp(date)
                        .strftime('%Y-%m-%d'))
                print(f'{project}: Last Modified {date}')
    
    return [project for date, project in project_list]

# Gather Submission Materials ---------------------------------------------

def gather_submission(project_path, main_file, support_files, output_dir, **kwargs):
    
    if kwargs.pop('prepend_project', False):
        output_dir = os.path.join(project_path, output_dir)
        
    output_root = Path(output_dir).parent
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    else: # clear the output directory
        if kwargs.get('fresh_start', True):
            if kwargs.get('verbose', True):
                print('Clearing the output directory:', output_dir)
            shutil.rmtree(output_dir)
            os.makedirs(output_dir, exist_ok=True)
    
    new_main = kwargs.pop('main_name', 'manuscript.tex')
    
    # Stitch (but don't yet write) main file .tex content
    content = stitch_tex_files(project_path, main_file, 
                                content_only=True, **kwargs)

    original_to_new = {} # file_path mappings
    
    #optional renaming schema for materials
    new_names = kwargs.pop('new_names', {})
    
    image_extensions = Image.registered_extensions()
    image_format = kwargs.pop('image_format', None)

    # Copy files to the output directory, flattening the structure
    for file_path in support_files:
        original_dir, filename = os.path.split(file_path)
        filename = new_names.get(filename, filename)
        new_path = os.path.join(output_dir, filename)

        # Check if there's a file name clash and handle it
        if not os.path.exists(new_path):
            base, ext = os.path.splitext(filename)
            count = 1 # add as suffix to new_path
            
            while os.path.exists(new_path):
                new_filename = f"{base}_{str(count).zfill(2)}{ext}"
                new_path = os.path.join(output_dir, new_filename)
                count += 1 # iter-update the file count

        # Copy the file
        src_path = os.path.join(project_path, file_path)
    
        shutil.copyfile(src_path, new_path)
        original_to_new[file_path] = new_path
        
    image_files = [file_path for file_path in original_to_new if 
                   os.path.splitext(file_path)[1] in image_extensions]
    
    if image_format is not None: # convert images to target format
        description = f'Converting Images to {image_format.upper()}'
        
        for file_path in tqdm(image_files, desc=description):
            if file_path.endswith(image_format): continue
            
            new_path = original_to_new[file_path]
            convert_image(new_path, image_format)
            
            _, src_ext = os.path.splitext(new_path)
            new_path = new_path.replace(src_ext, f'.{image_format}')
            
            original_to_new[file_path] = new_path # update the mapping
            
    last_bibliography = r'\\bibliography\{references\}'
                
    # Update references in the content
    for old_path, new_path in original_to_new.items():
        new_path = os.path.basename(new_path) # relative
        
        new_name, _ = os.path.splitext(new_path)
        old_name, _ = os.path.splitext(old_path)

        search_result = search_for_input(old_path, content, **kwargs)
        
        if search_result is not None:
            match_base = search_result['match_base']
            context = search_result['in_command']
            extension_included = '.' in match_base
            
            if extension_included: # update with path
                update = context.replace(old_path, new_path)
                
            else: # update with name only
                update = context.replace(old_name, new_name)
                
            if kwargs.get('exclude_comments', True):
                if context.startswith('%'):
                    continue # skip commented lines
                
            new_string = new_path if '.' in match_base else new_name
            
            if kwargs.get('verbose', False):
                print(f"Updating {match_base} to {new_string}"+
                      f" in {context}:\n  -> {update}")
            
            content = content.replace(context, update)
            
            if 'bibliography' in update:
                last_bibliography = copy(update)
            
    if kwargs.pop('stitch_bibtex', True):
        bibtex_files = get_bibtex_files(output_root, output_dir)
        output_file = os.path.join(output_dir, 'references.bib')
        
        if kwargs.get('verbose', False): 
            print(f'Stitching {len(bibtex_files)} to {output_file}...')
        
        stitch_bibtex_files(project_path, bibtex_files, output_file,
                            cleanup=True, dry_run=False)
        
        new_bibliography = "\\bibliography{references}"
        content = content.replace(last_bibliography, new_bibliography)
        
        if kwargs.get('verbose', True):
            print(f"Updating {last_bibliography} to {new_bibliography}")
                
    write_content(os.path.join(output_dir, new_main), content)

# Find Document Input -----------------------------------------------------

def get_command_regex(search, input_only=False):
    latex_commands = [r'\\input', r'\\usepackage', r'\\bibliography', r'\\includegraphics']
    if input_only: latex_commands = [r'\\input']
    command_pattern = f"({'|'.join(latex_commands)})"
    
    return (rf"(?:% *\s*)?{command_pattern}(?:\[[^\]]*\])?"+
            rf"\{{.*?\b{re.escape(search)}(\.\w+)?\b.*?\}}")

def search_for_input(file_path, content, **kwargs):
    base_name, extension = os.path.splitext(file_path)
    
    search_pattern = get_command_regex(base_name)
    matches = re.finditer(search_pattern, content)
        
    results = None # default to None
    all_results = [] # if multiple
    
    for match in matches:
        if kwargs.get('ignore_comments', True):
            if match.group(0).startswith('%'):
                continue # skip commented lines
            
        match_name = copy(base_name)
            
        if extension in match.group(0):
            match_name += extension
                
        results = {'match_base': match_name,
                   'in_command': match.group(0)}
        
        all_results += [results]
        
    if len(all_results) > 1:
        print('Warning: Multiple matches found for', file_path)

    return results # dictionary with match_context

def find_tex_inputs(project_dir, main_file='main.tex', depth=0, **kwargs):
    max_depth = kwargs.get('max_depth', 5)
    
    if depth > max_depth:
        print(f"Warning: Maximum recursion depth reached at {main_file}. Stopping.")
        return {}

    file_path = os.path.join(project_dir, main_file)
    if not os.path.exists(file_path):
        print(f"Warning: File not found: {file_path}. Skipping...")
        return {}

    with open(file_path, 'r') as file:
        content = file.read()

    # initialize the structure at the main file
    structure = {main_file: {"path": file_path,
                             "inputs": {}}}

    # Find all \input{} commands
    inputs = re.findall(r'(?:%\s*)?\\input\{(.+?)\}', content)
    
    for input_file in inputs:
        search_result = search_for_input(input_file, content, **kwargs)
        
        if search_result is None:
            continue # skip this file
        
        if not input_file.endswith('.tex'):
            input_file += '.tex'
        input_path = copy(input_file)
        if kwargs.get('prepend_path', False):
            input_path = os.path.join(os.path.dirname(file_path), input_file)
        
        # Recursively process the input file
        sub_structure = find_tex_inputs(project_dir, input_path, 
                                        depth+1, **kwargs)
        
        structure[main_file]["inputs"].update(sub_structure)

    return structure

def find_all_inputs(project_path, main_file, stitch_first=False, **kwargs):
    
    # List all non-hidden files recursively in the project path
    all_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, project_path)
            if not relative_path.startswith('.'):
                if not file == main_file:
                    all_files.append(relative_path)
                    
    main_filepath = os.path.join(project_path, main_file)
        
    if not stitch_first: # Read the contents of the main file
        content = read_content(main_filepath)
        
    else: # Stitch together all \inputs to main file first
        content = stitch_tex_files(project_path, main_file, 
                                    content_only=True, **kwargs)
        
    results = {} # Dictionary to hold the results

    for relative_path in all_files:
        search_result = search_for_input(relative_path, content, **kwargs)
        
        if search_result is not None:
            results[relative_path] = search_result
            
    if kwargs.get('exclusions', None):
        def check_exclusion(entry):
            return any(exc in entry for exc in kwargs['exclusions'])
        
        results = {key: value for key, value in results.items()
                   if not check_exclusion(key)}
        
    if kwargs.get('files_only', False):
        return list(results.keys()) # file_paths
    
    return results # dictionary with file paths and match context

# Stitch Tex Documents ----------------------------------------------------

def write_content(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
        
def read_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content # from document

def update_paths(project_path, tex_file, updates, **kwargs):
    content = read_content(os.path.join(project_path, tex_file))
    
    for previous, update in updates.items():
        if kwargs.get('verbose', False):
            print(f"Updating {previous} to {update}")
        content = content.replace(previous, update)
        
    write_content(os.path.join(project_path, tex_file), content)

def stitch_tex_files(project_dir, main_file='main.tex', output_file=None, **kwargs):
    comment_exclude = kwargs.pop('exclude_with_comment', [])
    exclusions = kwargs.get('exclude', [])
    
    verbose = kwargs.get('verbose', False)
    
    def process_file(file_info):
        file_path = file_info['path']
        with open(file_path, 'r') as file:
            content = file.read()

        # Replace \input{} commands
        for input_file, input_info in file_info['inputs'].items():
            if verbose: print(f"Stitching \\input{{{input_file}}}")
            base_name, extension = os.path.splitext(input_file)
            
            if any([exc in input_file for exc in exclusions]):
                continue # skip rewriting of this file
            
            search_pattern = get_command_regex(base_name, True)
                
            if any([exc in search_pattern for exc in comment_exclude]):
                sub_args = (search_pattern, lambda x: f"%{x.group(0)}")
                content = re.sub(*sub_args, content); continue
                
            search_result = search_for_input(input_file, content, **kwargs)
            if search_result is None:
                continue # skip this file
            
            input_content = process_file(input_info)
            
            content = re.sub(search_pattern, lambda m: input_content, content)

        return content

    # Process the main file (first key in the structure)
    structure = find_tex_inputs(project_dir, main_file, **kwargs)
    main_file_info = structure[main_file]
    
    stitched_content = process_file(main_file_info)
    
    if kwargs.pop('content_only', True) or output_file is None:
        return stitched_content # return directly

    # Write the stitched content to the output file
    if '/' in output_file: # create new subdir
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
    output_file = os.path.join(project_dir, output_file)
    
    with open(output_file, 'w') as file:
        file.write(stitched_content)

    print(f"Stitched file created: {output_file}")

# Manage Bibtex Files -----------------------------------------------------

def get_bibtex_dir(project_name, bibtex_dir='citation', **kwargs):
    overleaf_root = kwargs.pop('overleaf_root', None)
    overleaf_root = get_overleaf_root(overleaf_root)
    
    return os.path.join(overleaf_root, project_name, bibtex_dir)

def get_bibtex_files(project_path, bibtex_dir, other_dirs=[]):
    # Process target bibtex directories + files:
    directories, bibtex_files = [bibtex_dir], []
    
    if (other_dirs is not None and len(other_dirs) > 0):
        directories += [directory for directory in other_dirs]
        
    for directory in directories:
        search_string = f'{project_path}/{directory}'
        if directory is None:
            search_string = f'{project_path}'
            
        bibtex_files += glob(f'{search_string}/*.bib')
        
    # make all paths relative to project path
    bibtex_files = [os.path.relpath(file_path, project_path) 
                    for file_path in bibtex_files]
        
    return bibtex_files # from primary + other directories

def clean_bibtex(input_file_path, output_file_path=None):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_content = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line.startswith('%'):
            cleaned_content.append(line)

    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(cleaned_content)
    else: # Return as StringIO if no output_file specified
        return io.StringIO(''.join(cleaned_content))
    
def parse_bibtex_file(bibtex_content, backend='bibtexparser'):
    from pybtex.database import parse_string
    import bibtexparser # assumed version 1.X 
    
    if isinstance(bibtex_content, io.StringIO):
        bibtex_content.seek(0)  # Ensure buffer is ready to read from the beginning
        bibtex_content = bibtex_content.read()

    if backend == 'bibtexparser':
        with io.StringIO(bibtex_content) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        return bib_database
    elif backend == 'pybtex':
        bib_database = parse_string(bibtex_content, 'bibtex')
        return bib_database
    else: # raise error if backend not supported
        raise ValueError("Unsupported backend specified.")
    
# Stitch Bibtex Files -----------------------------------------------------

def stitch_bibtex_files(project_path, bibtex_files, output_file,
                        cleanup=False, dry_run=True, **kwargs):

    if kwargs.get('prepend_project', True):
        output_file = os.path.join(project_path, output_file)

        if isinstance(bibtex_files, str):
            if os.path.isdir(bibtex_files):
                if project_path[:1] not in bibtex_files:
                    bibtex_files = os.path.join(project_path, bibtex_files)

        else: # assume list of files
            for index in range(len(bibtex_files)):
                bibtex_files[index] = os.path.join(project_path, bibtex_files[index])
            
    if not dry_run: # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
    stitched_entries = {}
    files_to_process = []

    if isinstance(bibtex_files, str):
        if os.path.isdir(bibtex_files):
            files_to_process = get_bibtex_files(project_path, bibtex_files)
    
    else: # assume list of files
        files_to_process = copy(bibtex_files)

    # Read all .bib files and accumulate unique entries
    for file_path in files_to_process:
        with open(file_path, 'r') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
            
            if kwargs.get('verbose', False): # of entries fetched
                print(f"{len(bib_database.entries)} entries fetched",
                      f"from {os.path.basename(file_path)}")

            for entry in bib_database.entries:
                entry_id = entry.get('ID', None)
                if entry_id and entry_id not in bibtex_files:
                    stitched_entries[entry_id] = entry
                    
    if kwargs.get('verbose', False) or dry_run: 
        # report number of unique entries
        print(f"{len(stitched_entries)} unique entries across",
              f"{len(files_to_process)} bibtex files")

    if not dry_run: # Write unique entries to output_file
        with open(output_file, 'w') as write_file:
            writer = bibtexparser.bwriter.BibTexWriter()
            db = bibtexparser.bibdatabase.BibDatabase()
            
            db.entries = list(stitched_entries.values())
            write_file.write(writer.write(db)) # stitch
            
            print(f"Bibtex entries stitched to: {output_file}")
            
    else: # Report the output file name without writing
        print(f"Dry-Run: Entries stitched to {output_file}")

    if cleanup: # delete or move stitched files to backup
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        if kwargs.get('backup_dir', None) is not None:
            backup_dir = kwargs.get('backup_dir')
            output_dir = f'{Path(output_file).parent.parent}/{backup_dir}'
        
            backup_dir = f"{output_dir}/backup/{timestamp}"
            
            if not dry_run: # build the backup directory
                os.makedirs(backup_dir, exist_ok=True)
                for file_path in files_to_process:
                    dst = os.path.join(backup_dir, os.path.basename(file_path))
                    shutil.move(file_path, dst)
            
                    if kwargs.get('verbose', False):
                        print(f"Moving {file_path} to {dst}")
                        
            else: # report the move without actually moving
                for file_path in files_to_process:
                    print(f"Would move {file_path} to {backup_dir}")
                    
        else: # delete the stitched files
            for file_path in files_to_process:
                action_report = 'Would delete'
                
                if not dry_run: # delete file
                    os.remove(file_path)
                    action_report = 'Deleting'
                    
                if kwargs.get('verbose', False):
                    print(f"{action_report} {file_path}")
                
# Input / Image Conversion -----------------------------------------------------

def _make_opaque(img_input, bg_color=(255, 255, 255)):
    # if input is path, load it as image
    if isinstance(img_input, str):
        img = Image.open(img_input)
        
    else: # assume input is image
        img = copy(img_input)
    
    # Check if the image has an alpha channel
    if img.mode in ('RGBA', 'LA') or ('transparency' in img.info):
        # Create a new image with a white background
        background = Image.new(img.mode[:-1], img.size, bg_color)
        # Paste the image on the background (masking with itself)
        background.paste(img, img.split()[-1])
        image = background  # ... using the alpha channel as mask
    
    # Convert image to RGB 
    if img.mode != 'RGB':
        img = img.convert('RGB')
            
    return img # image updated with nontrasparent background

def convert_image(source_path, target_format, **kwargs):
    # Ensure the target format does not start with a dot
    if target_format.startswith('.'):
        target_format = target_format[1:]
    
    # Load the image with PIL:
    img = Image.open(source_path)
    
    if target_format in ['jpg', 'pdf']:
        img = _make_opaque(img)
    
    # Define the new filename
    base = os.path.splitext(source_path)[0]
    target_path = f"{base}.{target_format.lower()}"
    
    # Convert and save the image
    img.save(target_path, target_format.upper())
    
    if kwargs.pop('remove_original', True):
        os.remove(source_path)

    return target_path # return the new path