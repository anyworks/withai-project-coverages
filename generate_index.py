#!/usr/bin/env python3
"""
Script to automatically generate the root index.html for coverage reports.
Scans all project directories and creates a comprehensive index page.
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path


def find_project_directories(base_path="."):
    """Find all project directories (withai-* pattern)."""
    projects = []
    base = Path(base_path)
    
    for item in base.iterdir():
        if item.is_dir() and item.name.startswith("withai-"):
            projects.append(item)
    
    return sorted(projects, key=lambda p: p.name)


def get_project_metadata(project_path):
    """Extract metadata from a project directory."""
    metadata = {
        "name": project_path.name,
        "updated": None,
    }
    
    # Try to get last updated time from status.json if it exists
    status_file = project_path / "status.json"
    if status_file.exists():
        try:
            with open(status_file, "r") as f:
                status = json.load(f)
                if "timestamp" in status:
                    metadata["updated"] = status["timestamp"]
        except (IOError, json.JSONDecodeError, KeyError):
            pass
    
    # Fallback to directory modification time
    if not metadata["updated"]:
        try:
            mtime = os.path.getmtime(project_path)
            metadata["updated"] = datetime.fromtimestamp(mtime, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        except OSError:
            metadata["updated"] = "Unknown"
    
    return metadata


def generate_html(projects_metadata):
    """Generate the HTML content for index.html."""
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Generate project cards HTML
    project_cards = ""
    for project in projects_metadata:
        project_cards += f"""            <li class="project-card">
                <a href="{project['name']}/index.html">{project['name']}</a>
                <div class="project-meta">View detailed coverage report</div>
                <div class="timestamp">Updated: {project['updated']}</div>
            </li>
"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Coverage Reports</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            padding: 40px;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        .status-message {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 30px;
            color: #856404;
        }}
        .status-message.info {{
            background: #d1ecf1;
            border-color: #17a2b8;
            color: #0c5460;
        }}
        #project-list {{
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .project-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s ease;
        }}
        .project-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-color: #667eea;
        }}
        .project-card a {{
            text-decoration: none;
            color: #667eea;
            font-size: 1.3em;
            font-weight: 600;
            display: block;
            margin-bottom: 10px;
        }}
        .project-card a:hover {{
            color: #764ba2;
        }}
        .project-meta {{
            color: #666;
            font-size: 0.9em;
        }}
        .coverage-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: 600;
            margin-top: 8px;
        }}
        .coverage-high {{
            background: #28a745;
            color: white;
        }}
        .coverage-medium {{
            background: #ffc107;
            color: #333;
        }}
        .coverage-low {{
            background: #dc3545;
            color: white;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        .timestamp {{
            color: #999;
            font-size: 0.85em;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Project Coverage Reports</h1>
        <p class="subtitle">Test coverage reports for all projects</p>
        
        <div class="status-message info" id="status-message">
            ⏳ Coverage reports are being generated. Please check back in a few moments.
        </div>
        
        <ul id="project-list">
{project_cards}        </ul>
        
        <div class="footer">
            <p>Generated by <a href="https://github.com/anyworks/withai-project-coverages" target="_blank">withai-project-coverages</a></p>
            <p class="timestamp">Last updated: <span id="last-updated">{current_time}</span></p>
        </div>
    </div>
    
    <script>
        // Hide status message if projects exist
        const projectList = document.getElementById('project-list');
        const statusMessage = document.getElementById('status-message');
        if (projectList.children.length > 0) {{
            statusMessage.style.display = 'none';
        }}
    </script>
</body>
</html>
"""
    return html


def main():
    """Main function to generate index.html."""
    print("Scanning for project directories...")
    projects = find_project_directories()
    
    if not projects:
        print("No project directories found.")
        return
    
    print(f"Found {len(projects)} project(s):")
    
    projects_metadata = []
    for project in projects:
        metadata = get_project_metadata(project)
        projects_metadata.append(metadata)
        print(f"  - {metadata['name']} (Updated: {metadata['updated']})")
    
    print("\nGenerating index.html...")
    html_content = generate_html(projects_metadata)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✓ index.html has been generated successfully!")


if __name__ == "__main__":
    main()
