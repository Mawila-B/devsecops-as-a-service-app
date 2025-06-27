import subprocess
import os
import shutil

def run_all_scans(repo_url=None, local_path=None, output_dir="reports/outputs"):
    """
    Run all configured scanners (tfsec, trivy, gitleaks, zap).
    Either clone the repo_url or unzip local_path into a temp dir,
    then scan that directory.
    Save raw scanner outputs under output_dir.
    Return a dict of tool_name -> output_file_path.
    """

    scan_target_dir = os.path.join(output_dir, "scan_source")

    # Prepare scan source
    if repo_url:
        # Clone the repo (shallow clone)
        if os.path.exists(scan_target_dir):
            shutil.rmtree(scan_target_dir)
        clone_cmd = ["git", "clone", "--depth", "1", repo_url, scan_target_dir]
        subprocess.run(clone_cmd, check=True)
    elif local_path:
        # Assume zip file, unzip to scan_target_dir
        if os.path.exists(scan_target_dir):
            shutil.rmtree(scan_target_dir)
        os.makedirs(scan_target_dir, exist_ok=True)
        unzip_cmd = ["unzip", "-q", local_path, "-d", scan_target_dir]
        subprocess.run(unzip_cmd, check=True)
    else:
        raise Exception("Either repo_url or local_path must be provided")

    results = {}

    # Run tfsec (IaC scanner)
    tfsec_out = os.path.join(output_dir, "tfsec.json")
    tfsec_cmd = ["tfsec", scan_target_dir, "--format", "json", "--out", tfsec_out]
    subprocess.run(tfsec_cmd, check=True)
    results["tfsec"] = tfsec_out

    # Run trivy (SCA + misconfig)
    trivy_out = os.path.join(output_dir, "trivy.json")
    trivy_cmd = [
        "trivy",
        "fs",
        "--security-checks",
        "vuln,config",
        "--format",
        "json",
        "--output",
        trivy_out,
        scan_target_dir,
    ]
    subprocess.run(trivy_cmd, check=True)
    results["trivy"] = trivy_out

    # Run gitleaks (secret detection)
    gitleaks_out = os.path.join(output_dir, "gitleaks.json")
    gitleaks_cmd = [
        "gitleaks",
        "detect",
        "--source",
        scan_target_dir,
        "--report-format",
        "json",
        "--report-path",
        gitleaks_out,
    ]
    subprocess.run(gitleaks_cmd, check=True)
    results["gitleaks"] = gitleaks_out

    # Run zap (DAST)
    # For demo, we'll skip full zap scan (needs running app)
    # You can integrate zap baseline scan here if desired

    return results
