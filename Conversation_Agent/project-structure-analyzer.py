import os
import markdown

def analyze_project(project_path):
    def generate_tree(startpath):
        tree = []
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = '  ' * level
            tree.append(f"{indent}{os.path.basename(root)}/")
            for file in files:
                tree.append(f"{indent}  {file}")
        return '\n'.join(tree)

    def read_file_content(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    # Generate project structure
    structure = generate_tree(project_path)

    # Read and consolidate file contents
    consolidated_content = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                content = read_file_content(file_path)
                relative_path = os.path.relpath(file_path, project_path)
                consolidated_content.append(f"## {relative_path}\n\n```\n{content}\n```\n")
            except Exception as e:
                print(f"Error reading {file_path}: {str(e)}")

    # Create the output markdown file
    output = f"# Project Structure\n\n```\n{structure}\n```\n\n# File Contents\n\n"
    output += '\n'.join(consolidated_content)

    # Write to output file
    with open('project_analysis.md', 'w', encoding='utf-8') as f:
        f.write(output)

    print("Analysis complete. Results written to 'project_analysis.md'")

# Usage
project_path = './5'
analyze_project(project_path)
