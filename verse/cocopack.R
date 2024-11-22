if (!require(pacman)) {install.packages("pacman")}
pacman::p_load('this.path', 'scales', 'psych', 'progress',
               'viridis', 'cowplot', 'patchwork', 
               'patchwork', 'ggfortify', 'ggh4x','tidytext', 'tidyverse')

### plot utils -------------------------------------------------------

cocopack_theme <- function(which='default', text_size=24) {
  if (which == 'default') {
    theme_bw() + theme(
      text = element_text(size = text_size),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
    ) else {
      stop("Invalid cocopack theme; choose from c('default')")
    }
  }
}

closer_legend <- function(position='bottom') {
  theme(legend.justification="center",
        legend.position=position, 
        legend.box.margin=margin(-12,0,0,0))
}

view_ggplot2_shapes <- function() {
  data.frame(x = 1:25, y = rep(1, 25), shape = 0:24) %>%
  ggplot(aes(x = x, y = y)) +
    geom_point(aes(shape = factor(shape)), 
              size = 5, fill = "lightblue") +
    scale_shape_manual(values = 0:24) +
    labs(title = "ggplot2 Shape Palette", 
        shape = "Shape ID") +
    theme_minimal() + coord_fixed(ratio = 25) +
    theme(axis.title = element_blank(),
          axis.ticks = element_blank(),
          axis.text.y = element_blank(),
          axis.text.x = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank())
}

### data utils -----------------------------------------------------

read_csv_add_name <- function(file) {
  read_csv(file) %>% mutate(filename = file)
}

get_package_bibtex <- function(x) {
    print(x, bibtex = TRUE)
}

### boot utils -----------------------------------------------------

pacman::p_load('scales', 'progress', 'boot', 'ggstatsplot', 'tidyverse')

run_bootstrap <- function(data_frame, group_vars, boot_fn, times=1000, 
                          hypothesis=0, parse=TRUE, simplify=TRUE) {
  
  nested_data <- data_frame %>% ungroup() %>%
    group_by(across(all_of(group_vars))) %>% nest()
  
  total_groups <- nrow(nested_data)
  pb <- progress_bar$new(format = "Bootstrap: [:bar] :percent% eta: :eta", 
                         total = total_groups, clear = FALSE, width = 60)
  
  result <- nested_data %>%
    mutate(bootstrap_results = map(data, ~{
      on.exit(pb$tick())
      boot(data = .x, statistic = boot_fn, R = times)
    }))
  
  if (parse) {
    result <- result %>%
      mutate(bootstrap_ci = map(bootstrap_results, ~boot.ci(.x, type = "basic")),
             boot_stat = map_dbl(bootstrap_results, ~.x$t0),
             boot_lower_ci = map_dbl(bootstrap_ci, ~.x$basic[4]),
             boot_upper_ci = map_dbl(bootstrap_ci, ~.x$basic[5]),
             count_above_zero = map_dbl(bootstrap_results, ~sum(.x$t > 0)),
             count_below_zero = map_dbl(bootstrap_results, ~sum(.x$t < 0)),
             prop_above_zero = map_dbl(bootstrap_results, ~mean(.x$t > 0)),
             prop_below_zero = map_dbl(bootstrap_results, ~mean(.x$t < 0)),
             p_value = map_dbl(bootstrap_results, ~{
               obs_stat = hypothesis %||% .x$t0
               1 - (sum(abs(.x$t) >= abs(obs_stat)) / (times+1))
             }), # two_tailed test
             n_bootstraps = times,
             signif_alpha = case_when(
               p_value < 0.001 ~ 0.001,
               p_value < 0.01 ~ 0.01,
               p_value < 0.05 ~ 0.05,
               TRUE ~ NA_real_,
             ), # significance_at
             signif_label = case_when(
               p_value < 0.05 ~ "*",
               p_value < 0.01 ~ "**",
               p_value < 0.001 ~ "***",
               TRUE ~ "NS" # not significant
             )) %>% # remove bootstrap nested data
      select(-bootstrap_results, -bootstrap_ci, -data)
    
    if (simplify) {
      result <- result %>% select(-signif_alpha, signif_label) %>%
        select(-prop_below_zero, -prop_above_zero) %>%
        select(-count_above_zero, -count_below_zero, -n_bootstraps)
    }
    
    
  } else {
    result <- result %>% unnest(bootstrap_results) %>%
      mutate(boot_index = row_number()) %>% select(-data)
  }
  
  return(result)
}

label_significance <- function(results, p_col='p', alpha=0.5, alpha_low=0.001) {
    p_values = c(1e-5, 1e-4, 0.001, 0.01, 0.05) %>%
      keep(function(x) {x >= alpha_low & x <= alpha})
    
    labels = c(map(p_values, function(x) {glue('p > {x}')}), 'NS') %>%
      str_replace_all(fixed('0.'), '.')
    
    results %>% 
      add_significance(p.col = p_col, symbols = labels,
                       cutpoints = c(0, p_values, 1)) %>%
      rename_at(vars(ends_with('.signif')), str_replace, '.signif', '_signif')
  }

spearman_boot <- function(df, x_var, y_var, group_vars, R=1000, parse=TRUE) {
  # vectorized spearman correlation function
  spearman_corr <- function(data, indices=NULL, x_var, y_var) {
    if (is.null(indices)) {
      x <- data[[x_var]]
      y <- data[[x_var]]
    } else {
      x <- data[indices, ][[x_var]]
      y <- data[indices, ][[y_var]]
    }
    cor_test_result <- cor.test(x, y, method = "spearman")
    # Extract the correlation coefficient
    c(correlation = cor_test_result$estimate) 
  }

  # spearman with suppressed tie warnings
  boot_fn <- function(data, indices) {
    suppressWarnings(spearman_corr(data, indices, x_var, y_var))
  }
  
  boot_results <- run_bootstrap(df, group_vars, boot_fn, 
                                times=R, parse=parse)
  
  boot_results <- mutate(boot_results, method='spearman')
  
  if (parse) {
    boot_results <- boot_results %>%
      rename(cor = boot_stat,
             cor_lower = boot_lower_ci,
             cor_upper = boot_upper_ci)
  }
}