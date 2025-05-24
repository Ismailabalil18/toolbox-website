# Google AdSense Setup Guide for ToolBox Website

## Overview
This guide provides instructions on how to set up Google AdSense for your ToolBox website hosted on Netlify (toolbox.netlify.app).

## Why Google AdSense?
- **Compatibility:** Works well with Netlify static sites.
- **Revenue Potential:** Generally offers good revenue compared to other platforms.
- **Reliability:** Backed by Google, providing a stable platform.

## Steps to Set Up AdSense

**Note:** You need to complete these steps *after* the website is successfully deployed to toolbox.netlify.app.

1.  **Sign Up for Google AdSense:**
    *   Go to the [Google AdSense website](https://www.google.com/adsense/start/).
    *   Click "Get started".
    *   Enter your website URL: `https://toolbox.netlify.app`
    *   Enter your email address (preferably a Gmail account).
    *   Choose whether to receive helpful AdSense info via email.
    *   Click "Save and continue".
    *   Sign in to your Google Account.
    *   Select your country or territory.
    *   Review and accept the AdSense Terms and Conditions.
    *   Click "Start using AdSense".

2.  **Connect Your Site to AdSense:**
    *   AdSense will provide you with a piece of code (the AdSense code).
    *   You need to add this code to the `<head>` section of *every page* on your site where you want ads to appear.
    *   **How to add the code:**
        *   Edit the main layout template or individual page templates in your website code (e.g., `index.html`, `file/compressor.html`, `qrcode/generator.html`).
        *   Paste the AdSense code between the `<head>` and `</head>` tags.
        *   A good place is often right before the closing `</head>` tag or within the `head_seo.html` include file for easier management.
    *   After adding the code, commit and push the changes to your GitHub repository. Netlify will automatically redeploy the updated site.
    *   Go back to your AdSense account and confirm that you've placed the code on your site.

3.  **Wait for Review:**
    *   Google will review your site to check if it complies with AdSense Program policies. This process can take a few days, sometimes up to two weeks.
    *   Ensure your website has unique, high-quality content and provides a good user experience. The current tools (File Compressor, QR Code Generator) are a good start, but adding more content or tools might improve approval chances.
    *   You will receive an email once the review is complete.

4.  **Set Up Ads:**
    *   Once your site is approved, you can choose where and how ads appear.
    *   AdSense offers "Auto ads," where Google automatically places ads for you, or you can manually create ad units and place the corresponding code snippets where you want specific ads to show (e.g., in sidebars, between content sections).
    *   For Auto ads, you just need the main AdSense code in the `<head>`.
    *   For manual ad units, you'll paste additional code snippets into the `<body>` of your HTML templates where you want the ads.

## Important Considerations
*   **AdSense Policies:** Familiarize yourself with the [AdSense Program policies](https://support.google.com/adsense/answer/48182) to avoid violations.
*   **Content:** AdSense requires websites to have sufficient original content. Ensure your site meets these requirements.
*   **User Experience:** Don't overload your site with ads, as this can negatively impact user experience and potentially violate policies.

This guide provides the basic steps. Refer to the official Google AdSense documentation for more detailed information.
