# 🔑 GitHub SSH Setup Guide

## Step 1: Add SSH Key to GitHub

### 1. Copy Your SSH Public Key
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC8LkPr6RUN6O27JPXFH36Gl0Uj5FTttlYiKeD2i1hP+mLCA9/kvUKmPaMMEBZPPERXPEmIEjp0pmWGxhAUej2fXcHH2G6H64IL8Q0BKLw/CXV3+mHB5d9iTcseRZQu7qsd/QKhT3o1DrBiEFmw7fGh0HymnMt6AVQ8wuIFtgzy0ImmfMkzpTn6UYHxn4+dfQa6d+uGL9WDZ4agrrIIXeZUpOEil+3RjiyVF/9sZxnQVxRWTdMYpu/W9J00CVyZqRqG5dyEjsS6l4wcpdch0/r+5EpX1G5dIcdHvVELZcT8ZxBhtR+ClRZNaalAxIbvE0E2cFUKoTdRess2TWku0jjMenVz5xrNi6vLe6Moe9tCqacH/rDsrKS9wrQXobSgjVGRPxy/jyAM2MdFjzy2R0cqlfGkuy8qUpCNXxuuOgzH6wStjVKLWEmxdUI6AZ4CjutFHVkHatvKYsGLIXQ0BzFKmtbjH+GO9RuVaSzwQKsPI3hgPGuya/F30SpaDebPF6fBLPCMydOBdhA+r2glIq2VUxS2qZO1peJoGVdy6fQQUWCWYqeT19B/VsJ/76KcqWHVz0YKmslFQyntnfCqfHl8mvLqgqaboyPfwpuvRiVR2G8l3JUfci4qR33aIF4hweGf2xldHte88uWl1r0qJ6KwmfXbT1apk6+aBAaHHCmcbw== your_email@example.com
```

### 2. Go to GitHub SSH Settings
- Visit: https://github.com/settings/keys
- Click "New SSH key"

### 3. Add the Key
- **Title**: EHB Home Page SSH Key
- **Key type**: Authentication Key
- **Key**: Paste the SSH public key above
- Click "Add SSH key"

## Step 2: Test SSH Connection

After adding the key to GitHub, run:
```bash
ssh -T git@github.com
```

You should see: "Hi rafiehb555! You've successfully authenticated..."

## Step 3: Push Data to GitHub

Once SSH is working, run:
```bash
git push origin main
```

## 🔧 **Alternative: Use Personal Access Token**

If SSH doesn't work, you can use a Personal Access Token:

### 1. Create Personal Access Token
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select scopes: `repo`, `workflow`
- Copy the token

### 2. Use Token for Push
```bash
git remote set-url origin https://rafiehb555:YOUR_TOKEN@github.com/rafiehb555/EHB-HOME.git
git push origin main
```

## 📋 **Current Status**

- ✅ SSH Key Generated
- ✅ Git Remote Updated to SSH
- ⏳ Waiting for GitHub SSH Key Addition
- ⏳ Ready to Push Data

**Next Step**: Add the SSH key to your GitHub account, then we can push all the data!
