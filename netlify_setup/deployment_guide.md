# Netlify Deployment Guide for ToolBox Website

## Overview
This document outlines the steps to deploy the ToolBox website to Netlify with the subdomain toolbox.netlify.app.

## Prerequisites
- GitHub account
- Netlify account
- ToolBox website code (located in /home/ubuntu/website_project/clean_toolbox)

## Deployment Steps

### 1. Create a GitHub Repository
- Create a new GitHub repository named "toolbox-website"
- Initialize with README.md
- Set to public visibility

### 2. Push Website Code to GitHub
```bash
cd /home/ubuntu/website_project
git init
git add clean_toolbox/
git add netlify_setup/
git commit -m "Initial commit of ToolBox website"
git remote add origin https://github.com/yourusername/toolbox-website.git
git push -u origin main
```

### 3. Connect to Netlify
- Sign up/login to Netlify
- Click "New site from Git"
- Select GitHub as the Git provider
- Authorize Netlify to access your GitHub account
- Select the "toolbox-website" repository

### 4. Configure Build Settings
- Build command: Leave blank (static site)
- Publish directory: clean_toolbox/src
- Click "Deploy site"

### 5. Configure Custom Subdomain
- After deployment, go to "Site settings"
- Click "Change site name"
- Enter "toolbox" to get toolbox.netlify.app
- Save changes

### 6. Verify Deployment
- Check that the site is accessible at toolbox.netlify.app
- Test all functionality to ensure proper operation

## Post-Deployment
- Set up continuous deployment for automatic updates
- Configure custom domain (if purchased in the future)
- Add SSL certificate (automatically provided by Netlify)
