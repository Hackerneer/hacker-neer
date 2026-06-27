#!/usr/bin/env python3
# HACKER NEER v2.0 - Ultimate Instagram Gathering Tool
# YouTube: https://youtube.com/@hackerneer
# Educational Purpose Only

import instaloader
import time
import os
import json
import requests
from datetime import datetime
from colorama import init, Fore, Style
import threading

init(autoreset=True)

class HackerNeer:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.session_file = "hacker_neer_session.json"
        self.results = {}
        self.YOUTUBE_URL = "https://youtube.com/@hackerneer?si=OD82rZBgV2yzarAF"
        
    def banner(self):
        """Display cool banner"""
        banner_text = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════╗
{Fore.RED}║  {Fore.YELLOW}🔥 HACKER NEER v2.0 {Fore.RED}║
{Fore.RED}║  {Fore.CYAN}Instagram OSINT & Gathering Tool {Fore.RED}║
{Fore.RED}║  {Fore.GREEN}YouTube: {self.YOUTUBE_URL} {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════╝
{Fore.WHITE}
        """
        print(banner_text)
    
    def login(self, username=None, password=None):
        """Login to Instagram"""
        try:
            if not username:
                username = input(f"{Fore.CYAN}[?] Instagram Username: ")
                password = input(f"{Fore.CYAN}[?] Instagram Password: ")
            
            self.loader.login(username, password)
            print(f"{Fore.GREEN}[✓] Login successful as @{username}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[✗] Login failed: {e}")
            return False
    
    def get_profile_info(self, username):
        """Get complete profile data"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            data = {
                "Username": profile.username,
                "Full Name": profile.full_name,
                "Bio": profile.biography[:200] + "..." if len(profile.biography) > 200 else profile.biography,
                "External URL": profile.external_url,
                "Followers": profile.followers,
                "Following": profile.followees,
                "Posts": profile.mediacount,
                "Private": profile.is_private,
                "Verified": profile.is_verified,
                "Business": profile.is_business_account,
                "Business Category": profile.business_category_name if profile.is_business_account else "N/A",
                "Profile Pic URL": profile.profile_pic_url,
                "Joined": profile.profile_pic_url  # Approximate
            }
            return data
        except Exception as e:
            return {"Error": str(e)}
    
    def download_profile_pic(self, username, url):
        """Download profile picture"""
        try:
            filename = f"hacker_neer_{username}_dp.jpg"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return filename
            return None
        except:
            return None
    
    def get_recent_posts(self, username, limit=10):
        """Get recent posts with details"""
        posts = []
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            count = 0
            for post in profile.get_posts():
                if count >= limit:
                    break
                posts.append({
                    "Caption": post.caption[:150] + "..." if post.caption and len(post.caption) > 150 else post.caption,
                    "Likes": post.likes,
                    "Comments": post.comments,
                    "Date": post.date_utc.strftime("%Y-%m-%d %H:%M"),
                    "URL": f"https://instagram.com/p/{post.shortcode}",
                    "Hashtags": len([word for word in post.caption.split() if word.startswith('#')]) if post.caption else 0,
                    "Type": "Video" if post.is_video else "Image"
                })
                count += 1
            return posts
        except Exception as e:
            return {"Error": str(e)}
    
    def get_followers_list(self, username, limit=50):
        """Get followers usernames"""
        followers = []
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            count = 0
            for follower in profile.get_followers():
                if count >= limit:
                    break
                followers.append({
                    "Username": follower.username,
                    "Full Name": follower.full_name,
                    "Private": follower.is_private
                })
                count += 1
            return followers
        except Exception as e:
            return {"Error": str(e)}
    
    def get_following_list(self, username, limit=50):
        """Get following usernames"""
        following = []
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            count = 0
            for followee in profile.get_followees():
                if count >= limit:
                    break
                following.append({
                    "Username": followee.username,
                    "Full Name": followee.full_name,
                    "Private": followee.is_private
                })
                count += 1
            return following
        except Exception as e:
            return {"Error": str(e)}
    
    def get_hashtag_posts(self, hashtag, limit=10):
        """Search posts by hashtag"""
        posts = []
        try:
            for post in self.loader.get_hashtag_posts(hashtag):
                if len(posts) >= limit:
                    break
                posts.append({
                    "Owner": post.owner_username,
                    "Caption": post.caption[:100] + "..." if post.caption and len(post.caption) > 100 else post.caption,
                    "Likes": post.likes,
                    "Comments": post.comments,
                    "URL": f"https://instagram.com/p/{post.shortcode}"
                })
            return posts
        except Exception as e:
            return {"Error": str(e)}
    
    def download_stories(self, username, limit=5):
        """Download public stories"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            stories = []
            count = 0
            for story in self.loader.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    if count >= limit:
                        break
                    filename = f"story_{username}_{count}.jpg"
                    self.loader.download_storyitem(item, filename)
                    stories.append(f"Downloaded: {filename}")
                    count += 1
                if count >= limit:
                    break
            return stories if stories else ["No public stories found"]
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def get_post_comments(self, post_url, limit=20):
        """Get comments from a specific post"""
        try:
            shortcode = post_url.split('/p/')[1].split('/')[0]
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            comments = []
            for comment in post.get_comments():
                if len(comments) >= limit:
                    break
                comments.append({
                    "User": comment.owner.username,
                    "Text": comment.text[:150] + "..." if len(comment.text) > 150 else comment.text,
                    "Likes": comment.likes
                })
            return comments
        except Exception as e:
            return {"Error": str(e)}
    
    def compare_followers(self, username1, username2, limit=30):
        """Compare followers between two accounts"""
        print(f"{Fore.YELLOW}[+] Comparing followers...")
        followers1 = self.get_followers_list(username1, limit)
        followers2 = self.get_followers_list(username2, limit)
        
        if "Error" in followers1 or "Error" in followers2:
            return {"Error": "Could not fetch followers"}
        
        set1 = set([f['Username'] for f in followers1])
        set2 = set([f['Username'] for f in followers2])
        
        common = set1.intersection(set2)
        unique_to_1 = set1 - set2
        unique_to_2 = set2 - set1
        
        return {
            "Common": list(common),
            "Unique to @{}".format(username1): list(unique_to_1),
            "Unique to @{}".format(username2): list(unique_to_2)
        }
    
    def generate_html_report(self, username, data, posts, followers, following):
        """Generate beautiful HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"HackerNeer_{username}_{timestamp}.html"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Hacker Neer - @{username}</title>
    <style>
        body {{ font-family: Arial; background: #0a0a0a; color: #fff; padding: 20px; }}
        .container {{ max-width: 900px; margin: auto; background: #1a1a1a; padding: 20px; border-radius: 10px; }}
        .header {{ text-align: center; border-bottom: 2px solid #e1306c; padding-bottom: 20px; }}
        .header h1 {{ color: #e1306c; }}
        .card {{ background: #2a2a2a; padding: 15px; margin: 15px 0; border-radius: 8px; }}
        .stats {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; }}
        .stat-box {{ background: #333; padding: 10px; text-align: center; border-radius: 5px; }}
        .stat-value {{ font-size: 24px; color: #e1306c; font-weight: bold; }}
        .stat-label {{ font-size: 12px; color: #aaa; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; border-top: 1px solid #333; padding-top: 20px; }}
        .badge {{ background: #e1306c; padding: 3px 10px; border-radius: 20px; font-size: 12px; }}
        .youtube-link {{ color: #ff0000; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 HACKER NEER v2.0</h1>
            <p>Instagram Intelligence Report</p>
            <p>🎯 <a href="{self.YOUTUBE_URL}" target="_blank" class="youtube-link">Subscribe: @hackerneer</a></p>
        </div>
        
        <div class="card">
            <h2>📊 Profile: @{username}</h2>
            <div class="stats">
                <div class="stat-box"><div class="stat-value">{data.get('Followers', 0)}</div><div class="stat-label">Followers</div></div>
                <div class="stat-box"><div class="stat-value">{data.get('Following', 0)}</div><div class="stat-label">Following</div></div>
                <div class="stat-box"><div class="stat-value">{data.get('Posts', 0)}</div><div class="stat-label">Posts</div></div>
            </div>
            <p><strong>Bio:</strong> {data.get('Bio', 'N/A')}</p>
            <p><strong>Verified:</strong> {data.get('Verified', False)} | 
            <strong>Private:</strong> {data.get('Private', False)}</p>
        </div>
        
        <div class="card">
            <h2>📸 Recent Posts</h2>
            {"".join([f'''
            <div style="background:#333;padding:10px;margin:10px 0;border-radius:5px;">
                <p><strong>Post #{i+1}</strong> | {p.get('Type', 'Image')} | ❤️ {p.get('Likes', 0)} | 💬 {p.get('Comments', 0)}</p>
                <p style="color:#aaa;font-size:14px;">{p.get('Caption', 'No caption')[:200]}</p>
                <a href="{p.get('URL', '#')}" target="_blank" style="color:#e1306c;">View Post</a>
            </div>
            ''' for i,p in enumerate(posts) if isinstance(posts, list)])}
        </div>
        
        <div class="card">
            <h2>👥 Followers ({len(followers) if isinstance(followers, list) else 0})</h2>
            <p style="font-size:14px;color:#aaa;">{"".join([f'<span style="background:#444;padding:5px 10px;margin:5px;display:inline-block;border-radius:20px;">@{f["Username"]}</span> ' for f in followers[:20]])}</p>
        </div>
        
        <div class="footer">
            <p>🔒 Educational Purpose Only | Generated by Hacker Neer</p>
            <p>📺 <a href="{self.YOUTUBE_URL}" target="_blank" style="color:#ff0000;">YouTube: @hackerneer</a></p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filename
    
    def batch_process(self, usernames):
        """Process multiple usernames"""
        results = {}
        for username in usernames:
            print(f"\n{Fore.CYAN}[+] Processing @{username}...")
            data = self.get_profile_info(username)
            if "Error" not in data:
                posts = self.get_recent_posts(username, 5)
                followers = self.get_followers_list(username, 20)
                following = self.get_following_list(username, 20)
                results[username] = {
                    "data": data,
                    "posts": posts,
                    "followers": followers,
                    "following": following
                }
                print(f"{Fore.GREEN}[✓] Completed @{username}")
            time.sleep(2)  # Rate limiting
        return results
    
    def interactive_menu(self):
        """Main interactive menu"""
        while True:
            print(f"""
{Fore.YELLOW}┌─────────────────────────────────────────┐
│  {Fore.CYAN}1{Fore.WHITE}. Single Profile Scan              │
│  {Fore.CYAN}2{Fore.WHITE}. Hashtag Search                  │
│  {Fore.CYAN}3{Fore.WHITE}. Compare Two Accounts           │
│  {Fore.CYAN}4{Fore.WHITE}. Batch Scan (Multiple)          │
│  {Fore.CYAN}5{Fore.WHITE}. Download Stories               │
│  {Fore.CYAN}6{Fore.WHITE}. View Comments on Post          │
│  {Fore.CYAN}7{Fore.WHITE}. Exit                          │
└─────────────────────────────────────────┘
            """)
            
            choice = input(f"{Fore.GREEN}[?] Choose option: ")
            
            if choice == '1':
                username = input("[?] Target username: ")
                self.scan_single(username)
            
            elif choice == '2':
                hashtag = input("[?] Hashtag (without #): ")
                posts = self.get_hashtag_posts(hashtag, 10)
                print(f"\n{Fore.CYAN}Top Posts for #{hashtag}:")
                for i, post in enumerate(posts, 1):
                    print(f"{Fore.WHITE}{i}. @{post['Owner']} - ❤️ {post['Likes']} - {post['Caption'][:50]}")
            
            elif choice == '3':
                acc1 = input("[?] First username: ")
                acc2 = input("[?] Second username: ")
                comparison = self.compare_followers(acc1, acc2)
                print(f"\n{Fore.CYAN}Comparison Results:")
                for key, value in comparison.items():
                    print(f"{Fore.WHITE}{key}: {len(value)} users")
                    if len(value) <= 10:
                        print(f"  {', '.join(value)}")
            
            elif choice == '4':
                users = input("[?] Usernames (comma separated): ").split(',')
                users = [u.strip() for u in users]
                results = self.batch_process(users)
                print(f"\n{Fore.GREEN}[✓] Batch scan completed for {len(results)} accounts")
            
            elif choice == '5':
                username = input("[?] Target username: ")
                stories = self.download_stories(username, 5)
                for s in stories:
                    print(f"{Fore.GREEN}[+] {s}")
            
            elif choice == '6':
                url = input("[?] Post URL: ")
                comments = self.get_post_comments(url, 10)
                print(f"\n{Fore.CYAN}Top Comments:")
                for i, c in enumerate(comments, 1):
                    print(f"{Fore.WHITE}{i}. @{c['User']}: {c['Text'][:80]}")
            
            elif choice == '7':
                print(f"{Fore.RED}[!] Exiting... Thanks for using Hacker Neer!")
                break
            
            else:
                print(f"{Fore.RED}[!] Invalid choice")
            
            input(f"\n{Fore.YELLOW}[Press Enter to continue...]")
            os.system('clear' if os.name == 'posix' else 'cls')
    
    def scan_single(self, username):
        """Scan single profile with full report"""
        print(f"\n{Fore.YELLOW}[+] Scanning @{username}...")
        
        # Get data
        data = self.get_profile_info(username)
        if "Error" in data:
            print(f"{Fore.RED}[✗] {data['Error']}")
            return
        
        posts = self.get_recent_posts(username, 8)
        followers = self.get_followers_list(username, 30)
        following = self.get_following_list(username, 30)
        
        # Download profile pic
        dp_file = self.download_profile_pic(username, data.get('Profile Pic URL', ''))
        if dp_file:
            print(f"{Fore.GREEN}[✓] Profile pic saved: {dp_file}")
        
        # Display results
        print(f"\n{Fore.CYAN}📊 Profile Data:")
        for key, value in data.items():
            if key != 'Profile Pic URL':
                print(f"{Fore.WHITE}  {key}: {value}")
        
        print(f"\n{Fore.CYAN}📸 Recent Posts:")
        for i, post in enumerate(posts[:5], 1):
            print(f"{Fore.WHITE}  {i}. ❤️ {post['Likes']} | 💬 {post['Comments']} | {post['Date']}")
        
        # Generate HTML report
        report_file = self.generate_html_report(username, data, posts, followers, following)
        print(f"\n{Fore.GREEN}[✓] HTML Report saved: {report_file}")
        
        # Save summary
        summary_file = f"HackerNeer_{username}_summary.txt"
        with open(summary_file, 'w') as f:
            f.write(f"Hacker Neer - @{username}\n")
            f.write("="*50 + "\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
            f.write("\nTop Followers:\n")
            for fuser in followers[:10]:
                f.write(f"  @{fuser['Username']}\n")
        
        print(f"{Fore.GREEN}[✓] Summary saved: {summary_file}")

def main():
    hacker = HackerNeer()
    hacker.banner()
    
    # Login option
    login_choice = input(f"{Fore.YELLOW}[?] Login to Instagram? (y/n): ").lower()
    if login_choice == 'y':
        hacker.login()
    
    hacker.interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupted")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")