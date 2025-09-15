# 🔐 AWS Setup Guide for Fantasy Football Roast Agent

This guide walks you through setting up AWS credentials and Bedrock permissions for the Fantasy Football Roast Agent.

## 🎯 **What You Need**

1. **AWS Account** with access to Amazon Bedrock
2. **IAM User** with programmatic access (Access Key + Secret Key)
3. **Bedrock Model Access** (specifically Claude models)

## 📋 **Step-by-Step Setup**

### **Step 1: Create AWS IAM User (if you don't have one)**

1. **Log into AWS Console** → Go to IAM
2. **Create User**:
   - Click "Users" → "Create user"
   - Username: `fantasy-roast-agent` (or your preference)
   - Access type: ✅ **Programmatic access**
   - ❌ AWS Management Console access (not needed)

3. **Create Access Keys**:
   - Click on your new user
   - Go to "Security credentials" tab
   - Click "Create access key"
   - Choose "Command Line Interface (CLI)"
   - Copy your **Access Key ID** and **Secret Access Key**
   - ⚠️ **IMPORTANT**: Save these securely - you can't see the secret again!

### **Step 2: Set Up Bedrock Permissions**

1. **Create Custom Policy**:
   - In IAM, click "Policies" → "Create policy"
   - Click "JSON" tab
   - Copy the contents from `bedrock_permissions.json` in this directory
   - Name it: `FantasyFootballBedrockAccess`
   - Click "Create policy"

2. **Attach Policy to User**:
   - Go back to your IAM user
   - Click "Add permissions" → "Attach policies directly"
   - Search for `FantasyFootballBedrockAccess`
   - Select it and click "Add permissions"

### **Step 3: Enable Bedrock Model Access**

1. **Go to Amazon Bedrock Console**
2. **Model Access**:
   - In left sidebar, click "Model access"
   - Click "Request model access"
   - Find **Anthropic Claude** models
   - Select: ✅ Claude 3.7 Sonnet, ✅ Claude 3.5 Sonnet
   - Click "Request model access"
   - Wait for approval (usually instant for Claude models)

### **Step 4: Configure Environment Variables**

Run the setup script we created:

```bash
# Make the script executable
chmod +x setup_aws.sh

# Run the setup
./setup_aws.sh
```

**Or set manually:**

```bash
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
export AWS_DEFAULT_REGION="us-west-2"
```

**To make permanent, add to your shell profile:**

```bash
# For bash users
echo 'source /path/to/sleeper-fantasy-football-recommendation-agent/.env' >> ~/.bashrc

# For zsh users  
echo 'source /path/to/sleeper-fantasy-football-recommendation-agent/.env' >> ~/.zshrc
```

## ✅ **Verification Steps**

### **Test AWS Connection**
```bash
# Test if AWS credentials work
aws sts get-caller-identity
```

Should return your user info (User ID, Account, ARN).

### **Test Bedrock Access**
```bash
# List available models
aws bedrock list-foundation-models --region us-west-2
```

Should show Anthropic Claude models in the list.

### **Test Roast Agent Setup**
```bash
# Run our test script
python test_setup.py
```

Should show all tests passing.

## 🔧 **Troubleshooting**

### **"Access Denied" Errors**
- ✅ Check that your IAM policy is attached to the user
- ✅ Verify Bedrock model access is enabled
- ✅ Make sure you're using the correct region (us-west-2)

### **"Model Not Found" Errors**
- ✅ Request access to Claude models in Bedrock console
- ✅ Check that model ID in config.py matches available models
- ✅ Try a different region if models aren't available

### **"Credentials Not Found" Errors**
- ✅ Run `source .env` to load environment variables
- ✅ Check that AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set
- ✅ Verify credentials haven't expired

### **Rate Limiting**
- ✅ Bedrock has default quotas - request increases if needed
- ✅ Add delays between API calls if hitting limits

## 💰 **Costs**

**Bedrock Claude 3.7 Sonnet Pricing (us-west-2):**
- Input: ~$3.00 per 1M tokens
- Output: ~$15.00 per 1M tokens

**Estimated cost per roast report:** ~$0.10 - $0.50
(Reports are ~500-2000 tokens input, ~1000-3000 tokens output)

## 🔒 **Security Best Practices**

1. **Least Privilege**: Only grant necessary Bedrock permissions
2. **Rotate Keys**: Regularly rotate your access keys
3. **Environment Variables**: Never commit credentials to git
4. **Monitor Usage**: Check AWS CloudTrail for API usage
5. **Budget Alerts**: Set up billing alerts for unexpected costs

## 🚀 **Ready to Roast!**

Once everything is set up:

```bash
# Install final dependencies
pip install strands duckduckgo-search

# Test everything works
python test_setup.py

# List your league members
python run_roast.py --list-users

# Generate your first savage roast report
python run_roast.py --target "armanpopli"
```

The report will be saved to the `reports/` directory as a beautiful HTML file with maximum snark! 🔥

---

**Need help?** Check the main README.md or create an issue in the repository. 