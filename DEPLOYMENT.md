# 🚀 Deployment Guide

Deploy your Financial Literacy Simulator to the cloud for easy access during your live demo and classroom sessions.

## Option 1: Streamlit Community Cloud (Recommended - FREE)

### Easiest and fastest option - no credit card required!

**Step 1: Prepare Your Repository**
- Ensure your GitHub repository is public
- Verify all files are committed and pushed:
  - `dashboard.py`
  - `financial_simulator.py`
  - `requirements.txt`
  - `.streamlit/config.toml`

**Step 2: Deploy on Streamlit Cloud**
1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository: `mukeshk01/Financial-Literacy`
4. Select branch: `main`
5. Select file: `dashboard.py`
6. Click "Deploy!"

**Step 3: Access Your App**
- Your app will be live in ~2-3 minutes at:
  ```
  https://share.streamlit.io/mukeshk01/Financial-Literacy/main/dashboard.py
  ```

**Deployment Tips:**
- Custom URL: Available with Streamlit+ ($10/month)
- Free tier: 3 apps, 1GB storage, 1 CPU core
- Apps sleep after 30 minutes of inactivity (auto-restart on access)

---

## Option 2: Heroku Deployment

### Classic cloud platform with simple deployment

**Step 1: Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
# Verify installation
heroku --version
```

**Step 2: Create Heroku App**
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Or use automatic name generation
heroku create
```

**Step 3: Add Procfile**
Create a file named `Procfile` in your repository root:
```
web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

**Step 4: Add .gitignore**
Create `.gitignore` if not present:
```
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.env
.DS_Store
```

**Step 5: Deploy**
```bash
# Add and commit changes
git add .
git commit -m "Add deployment files"

# Push to Heroku
git push heroku main

# View logs
heroku logs --tail
```

**Step 6: Access Your App**
```
https://your-app-name.herokuapp.com
```

**Note:** Heroku free tier is no longer available (as of Nov 2022). Paid dyno starts at $7/month.

---

## Option 3: Docker + Cloud Run (Google Cloud)

### Most flexible option with container deployment

**Step 1: Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "dashboard.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

**Step 2: Create .dockerignore**
```
__pycache__
*.pyc
.git
.gitignore
README.md
.env
```

**Step 3: Build and Test Locally**
```bash
# Build image
docker build -t financial-simulator .

# Run container
docker run -p 8080:8080 financial-simulator
```

**Step 4: Deploy to Google Cloud Run**
```bash
# Install gcloud CLI (https://cloud.google.com/sdk/docs/install)

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy financial-simulator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Your app will be available at the provided URL
```

---

## Option 4: Local Network Demo (For Classroom)

### Share on local network during live session

**Step 1: Install and Run**
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

**Step 2: Find Your IP Address**
```bash
# On macOS/Linux
ifconfig | grep "inet "

# On Windows
ipconfig
```

**Step 3: Share URL with Students**
```
http://YOUR_IP_ADDRESS:8501
```

Students on the same network can now access the dashboard!

**Tip:** Use a tool like [ngrok](https://ngrok.com) to expose local server to internet:
```bash
ngrok http 8501
```

---

## Performance Optimization

### For 50+ students accessing simultaneously:

1. **Streamlit Cloud Limits**
   - Free tier: 1 CPU, may timeout with 50+ concurrent users
   - Use Streamlit+ or alternative

2. **Recommended Setup for Large Class**
   - Heroku with Eco dyno ($5/month) or higher
   - Multiple instances load-balanced
   - Separate instance per small group (10-15 students)

3. **Database Integration** (Optional)
   - Store session data in Firebase/Supabase
   - Enable persistent progress tracking
   - Create leaderboard for healthy competition

---

## Session Demo Setup

### Live Classroom Tips:

**Before Demo:**
```bash
# Test locally
streamlit run dashboard.py

# Share screen or projection URL
# Prepare talking points for each section
```

**During Demo:**
1. Open dashboard at full screen
2. Choose "Student" scenario (most relatable)
3. Show each feature step-by-step:
   - Monthly advancement
   - Investment decisions
   - Goal tracking
   - Visual charts
4. Let students suggest decisions
5. Highlight consequences of choices

**Interactive Elements:**
- Student 1: Decides investment amount
- Student 2: Decides debt payment
- Student 3: Sets a financial goal
- Whole class: Observes outcomes together

---

## Troubleshooting Deployment

### Issue: App crashes on startup
```bash
# Check requirements.txt has correct versions
pip install -r requirements.txt --upgrade

# Test locally first
streamlit run dashboard.py
```

### Issue: Slow performance
- Reduce historical data display
- Increase cache settings
- Use smaller update intervals

### Issue: Out of memory
- Clear session cache
- Reduce number of concurrent simulations
- Use database instead of in-memory storage

---

## Monitoring and Maintenance

### After Deployment:

1. **Monitor Performance**
   - Check response times
   - Monitor memory usage
   - Track error logs

2. **Collect Feedback**
   - Student experience survey
   - Feature requests
   - Bug reports

3. **Update Regularly**
   - Add new scenarios based on feedback
   - Improve visualizations
   - Fix reported issues

---

## Cost Comparison

| Platform | Cost | Pros | Cons |
|----------|------|------|------|
| **Streamlit Cloud** | FREE | Easiest setup, instant deploy | Limited features in free tier |
| **Heroku** | $7-50/month | Reliable, good uptime | No longer has free tier |
| **Google Cloud Run** | $0-10/month | Pay-per-use, scalable | Requires account setup |
| **AWS/Azure** | $5-50+/month | Enterprise-grade, powerful | Complex setup |
| **Local Network** | FREE | Full control, instant | Limited to classroom network |

---

## Recommended Setup for Your Use Case

**For Small Class (< 30 students):**
→ Use **Streamlit Community Cloud** (FREE)

**For Large Class (30-100 students):**
→ Use **Google Cloud Run** with persistent storage ($5-10/month)

**For Live Demo in Classroom:**
→ Use **Local Network** (free) with ngrok for remote access

---

## Quick Deploy Commands

```bash
# Streamlit Cloud (GitHub required)
# Just push code and deploy from https://share.streamlit.io

# Google Cloud Run
git clone https://github.com/mukeshk01/Financial-Literacy.git
cd Financial-Literacy
gcloud run deploy financial-literacy --source . --platform managed --region us-central1

# Local Network Demo
pip install -r requirements.txt
streamlit run dashboard.py
```

Happy deploying! 🚀
