import os
import time
import jwt
import requests
from flask import Flask, request, jsonify
from github import Github
from openai import OpenAI




app = Flask(__name__)

# GitHub App details
APP_ID = ""  
PRIVATE_KEY_PATH = "code-reviewer.pem"  
INSTALLATION_ID = ""  


client = OpenAI(api_key="")


def generate_jwt():
    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()


    payload = {
        "iat": int(time.time()),  
        "exp": int(time.time()) + 60,  
        "iss": APP_ID  
    }

    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")
    return jwt_token


def get_installation_access_token():
    jwt_token = generate_jwt()


    url = f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, headers=headers)

    if response.status_code == 201:
        return response.json()["token"]
    else:
        raise Exception(f"Failed to get installation access token: {response.status_code} {response.text}")


def get_github_client():
    token = get_installation_access_token()
    g = Github(token)
    return g


def get_code_review(diff):
    prompt = f"""
    Please review the following code and provide feedback. Look for areas of improvement, 
    such as readability, code style, potential bugs, security issues, and performance concerns.
    
    Code Diff:
    {diff}
    """
    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": "You are a helpful code reviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def post_review_feedback(pr, feedback):
    pr.create_issue_comment(f"### Code Review Feedback:\n{feedback}")


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get("action")

    if action in ["opened", "edited", "synchronize"]:
        pr_number = data['pull_request']['number']
        repo_name = data['repository']['full_name']
        
  
        g = get_github_client()  
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        files = pr.get_files()
        pr_diff = "\n".join([file.patch for file in files])

        review_feedback = get_code_review(pr_diff)


        post_review_feedback(pr, review_feedback)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4000)
