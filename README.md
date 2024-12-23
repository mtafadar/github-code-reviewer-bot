# GitHub Code Reviewer Bot

This is a POC where I tested OpenAI GPT-4 model as a code reviewer by creating a GitHub bot.

## Getting Started

To replicate this POC and create your own GitHub Code Reviewer Bot, follow the steps below:

---

## Step 1: Create a GitHub App

1. Go to [GitHub Developer Settings](https://github.com/settings/apps) and create a new GitHub App. 
   - Name it something like "Code Reviewer" or whatever you want the bot name to be

2. After creating the GitHub App, make sure to save the following details:
   - **App ID**
   - **Private Key** (download the `.pem` file)
   - **Installation ID**

These details will be required later. 

---

## Step 2: Set Up OpenAI Account

1. Create an account on [OpenAI](https://platform.openai.com/).
2. Add funds to your account to make sure that  the API Key works properly.

---

## Step 3: Install and Configure ngrok

1. Sign up for an account on [ngrok](https://ngrok.com/).
2. Follow the setup and installation documentation provided by ngrok to install it locally. 

ngrok will allow you to expose your local bot to the internet for testing purposes.

---

## Step 4: Clone and Configure the Code

1. Clone this repository to your local machine.

2. Replace the placeholder values in the following section of `github-bot.py` with your actual configuration:

   ```python
   APP_ID = "" 
   PRIVATE_KEY_PATH = "code-reviewer.pem"  # Path to your private key file
   INSTALLATION_ID = ""  
   client = OpenAI(api_key="")  
   ```

3. Run the bot using:
   ```bash
   python github-bot.py
   ```

4. Let Flask run in one terminal and open another terminal to start ngrok:
   ```bash
   ngrok http 4000
   ```

---

## Step 5: Add Webhook to Your Repository

1. Navigate to the repository where you want to add the bot.
2. Go to **Settings** > **Webhooks**.
3. Add a new webhook using the HTTPS URL provided by ngrok

Example webhook setup:

![webhook-setup](/images/webhool-setup.png)

---

## Testing the Bot

1. Create a pull request in the repository where the bot is configured.
2. Check the ngrok logs to verify if the POST request is successful.
3. If successful, the bot should add a review comment automatically. For example:

![code-review](/images/code-review.png)
