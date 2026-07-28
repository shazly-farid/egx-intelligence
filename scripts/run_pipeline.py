#!/usr/bin/env python3
"""
Main orchestration script for the EGX Intelligence system.
Coordinates data fetching, analysis, and report generation.
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class EGXIntelligenceOrchestrator:
    """
    Orchestrates the entire EGX Intelligence pipeline.
    """
    
    def __init__(self, data_dir: str = "data", reports_dir: str = "reports"):
        """
        Initialize the orchestrator.
        
        Args:
            data_dir: Directory for storing fetched data
            reports_dir: Directory for storing generated reports
        """
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.scripts_dir = Path("scripts")
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
        self.timestamp = datetime.now()
        self.date_str = self.timestamp.strftime("%Y-%m-%d")
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamps."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def run_script(self, script_name: str, args: Dict) -> bool:
        """
        Run a Python script with given arguments.
        
        Args:
            script_name: Name of the script to run
            args: Dictionary of command-line arguments
        
        Returns:
            True if successful, False otherwise
        """
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            self.log(f"Script not found: {script_path}", "ERROR")
            return False
        
        cmd = ["python3", str(script_path)]
        for key, value in args.items():
            cmd.append(f"--{key}")
            cmd.append(str(value))
        
        self.log(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.log(f"✓ {script_name} completed successfully")
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"✗ {script_name} failed with error code {e.returncode}", "ERROR")
            if e.stderr:
                print(e.stderr)
            return False
        except Exception as e:
            self.log(f"✗ Exception running {script_name}: {str(e)}", "ERROR")
            return False
    
    def fetch_egx_announcements(self) -> bool:
        """Fetch EGX announcements."""
        self.log("Step 1/6: Fetching EGX announcements...")
        
        output_file = self.data_dir / f"egx_announcements_{self.date_str}.json"
        
        args = {
            "output": str(output_file)
        }
        
        return self.run_script("fetch_egx_announcements.py", args)
    
    def fetch_fra_announcements(self) -> bool:
        """Fetch FRA announcements."""
        self.log("Step 2/6: Fetching FRA announcements...")
        
        output_file = self.data_dir / f"fra_announcements_{self.date_str}.json"
        
        args = {
            "output": str(output_file)
        }
        
        return self.run_script("fetch_fra_announcements.py", args)
    
    def fetch_financial_news(self) -> bool:
        """Fetch financial news."""
        self.log("Step 3/6: Fetching financial news...")
        
        output_file = self.data_dir / f"financial_news_{self.date_str}.json"
        
        args = {
            "output": str(output_file),
            "sources": "mubasher,arab-finance,al-borsa,hapi"
        }
        
        return self.run_script("fetch_financial_news.py", args)
    
    def analyze_signals(self) -> bool:
        """Analyze signals from fetched data."""
        self.log("Step 4/6: Analyzing signals...")
        
        egx_file = self.data_dir / f"egx_announcements_{self.date_str}.json"
        fra_file = self.data_dir / f"fra_announcements_{self.date_str}.json"
        news_file = self.data_dir / f"financial_news_{self.date_str}.json"
        output_file = self.data_dir / f"analysis_{self.date_str}.json"
        
        # Find previous report if it exists
        previous_report = None
        reports = sorted(self.reports_dir.glob("report_*.md"))
        if reports:
            previous_report = str(reports[-1])
        
        # Check if all input files exist
        for file in [egx_file, fra_file, news_file]:
            if not file.exists():
                self.log(f"Input file not found: {file}", "WARNING")
                # Create empty placeholder
                with open(file, 'w') as f:
                    json.dump({"announcements": [], "news": []}, f)
        
        args = {
            "egx-data": str(egx_file),
            "fra-data": str(fra_file),
            "news-data": str(news_file),
            "output": str(output_file)
        }
        
        if previous_report:
            args["previous-report"] = previous_report
        
        return self.run_script("analyze_signals.py", args)
    
    def generate_report(self) -> bool:
        """Generate the final report."""
        self.log("Step 5/6: Generating report...")
        
        analysis_file = self.data_dir / f"analysis_{self.date_str}.json"
        output_file = self.reports_dir / f"report_{self.date_str}.md"
        
        # Check if analysis file exists
        if not analysis_file.exists():
            self.log(f"Analysis file not found: {analysis_file}", "WARNING")
            # Create empty placeholder
            with open(analysis_file, 'w') as f:
                json.dump({
                    "egx_signals": {"bullish": [], "bearish": [], "neutral": []},
                    "fra_signals": {},
                    "news_signals": {},
                    "trading_signals": [],
                    "summary": {}
                }, f)
        
        args = {
            "analysis": str(analysis_file),
            "date": self.date_str,
            "output": str(output_file)
        }
        
        return self.run_script("generate_report.py", args)
    
    def create_summary(self) -> bool:
        """Create a summary of all generated files."""
        self.log("Step 6/6: Creating execution summary...")
        
        summary = {
            "execution_date": self.date_str,
            "execution_time": datetime.now().isoformat(),
            "data_files": [],
            "report_files": []
        }
        
        # List data files
        for file in sorted(self.data_dir.glob(f"*_{self.date_str}.json")):
            summary["data_files"].append({
                "name": file.name,
                "size": file.stat().st_size,
                "path": str(file)
            })
        
        # List report files
        for file in sorted(self.reports_dir.glob(f"report_{self.date_str}.md")):
            summary["report_files"].append({
                "name": file.name,
                "size": file.stat().st_size,
                "path": str(file)
            })
        
        summary_file = self.reports_dir / f"summary_{self.date_str}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.log(f"✓ Summary saved to {summary_file}")
        return True
    
    def run_pipeline(self, steps: List[str] = None) -> bool:
        """
        Run the complete pipeline.
        
        Args:
            steps: List of steps to run (default: all)
        
        Returns:
            True if all steps completed successfully
        """
        pipeline_steps = [
            ("fetch_egx", self.fetch_egx_announcements),
            ("fetch_fra", self.fetch_fra_announcements),
            ("fetch_news", self.fetch_financial_news),
            ("analyze", self.analyze_signals),
            ("report", self.generate_report),
            ("summary", self.create_summary)
        ]
        
        if steps:
            pipeline_steps = [(name, func) for name, func in pipeline_steps if name in steps]
        
        self.log(f"Starting EGX Intelligence Pipeline ({len(pipeline_steps)} steps)")
        self.log("=" * 60)
        
        results = {}
        for step_name, step_func in pipeline_steps:
            try:
                result = step_func()
                results[step_name] = result
                if not result:
                    self.log(f"Pipeline stopped at step: {step_name}", "WARNING")
                    break
            except Exception as e:
                self.log(f"Unexpected error in {step_name}: {str(e)}", "ERROR")
                results[step_name] = False
                break
        
        self.log("=" * 60)
        
        # Print summary
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        self.log(f"Pipeline Summary: {success_count}/{total_count} steps completed successfully")
        
        for step_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            self.log(f"  {status}: {step_name}")
        
        return all(results.values())

def main():
    parser = argparse.ArgumentParser(description="EGX Intelligence Pipeline Orchestrator")
    parser.add_argument("--data-dir", default="data", help="Data directory (default: data)")
    parser.add_argument("--reports-dir", default="reports", help="Reports directory (default: reports)")
    parser.add_argument("--steps", help="Comma-separated list of steps to run (default: all)")
    
    args = parser.parse_args()
    
    orchestrator = EGXIntelligenceOrchestrator(
        data_dir=args.data_dir,
        reports_dir=args.reports_dir
    )
    
    steps = None
    if args.steps:
        steps = [s.strip() for s in args.steps.split(",")]
    
    success = orchestrator.run_pipeline(steps)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
