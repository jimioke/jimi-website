---
author: jimioke
title: "Fixing Gem Install Issues in Fedora"
date: 2025-09-24T11:50:53-05:00
link: https://people.umass.edu/jimi/wrotelearning/fixing-gem-install-fedora/
slug: fixing-gem-install-fedora
categories:
- fedora
- ruby
- gems
---


<style>
.hljs {
    background: #ffffff !important;
    border: 1px solid #e1e1e1;
}
</style>

I was recently struggling with upgrading rubygems on my Fedora 41 machine. On this specific machine, I could not run `bundle exec jekyll serve --livereload` to view changes to my course [website](https://probstats.narslab.org/) locally. Specifically, running `gem update --system` or `gem install` was returning an error, as the process would fail when trying to install the [bigdecimal](https://rubygems.org/gems/bigdecimal/versions/1.2.7?locale=en) library:

```
An error occurred while installing bigdecimal (3.2.3), and Bundler cannot continue.
```

I searched online for a fix. It seemed some C libraries were missing, but none of the recommended packages were available, until I stumbled upon [redhat-rpm-config](https://packages.fedoraproject.org/pkgs/redhat-rpm-config/redhat-rpm-config/index.html). Installing this solved my problems:


```
sudo dnf install redhat-rpm-config
```

From there, I was able update rubygem and happily run `jekyll serve`!