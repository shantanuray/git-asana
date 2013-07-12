GitAsana
=========
Git repo: https://github.com/shantanuray/git-asana

Modified from git-asana integration made by  Pawel Zubrycki (https://github.com/Aulos/git-asana)

Requirements for git-asana integration:
 (a) List existing task IDs from asana
 (b) Create commits referencing task ID that will be updated as comments in asana tasks
 (c) Close tasks at successful pull request

Usage should as simple as:
    $ git-asana [No Arguments]
        will set project, workspace details and then display list of your tasks
    $ git-asana l, list
        will display list of tasks
    $ git-asana s, set <task id>
        will set the current task associated with commits to task id by using environment variable ASANA_TASK_ID. It'll add subsequent comments to selected task on Asana automatically.
    $ git-asana c, complete
        will close the task on asana and clear the environment variable ASANA_TASK_ID

I will be using .git-asana-config at the root of each repo to save information about project, workspace and current feature task. User can create this file with following information and structure:
    {
        "project": "<Project name>",
        "workspace": "<Workspace name>"
    }
After calling git-asana the first time, program will append respective is to the file by fetching it from :
    {
        "project": "<Project name>",
        "project_id": "<Project ID>",
        "workspace": "<Workspace name>",
        "workspace_id": "<Workspace ID>"
    }
Else this information can be set by calling git-asana without any arguments. A file .git-asana-config will be created automatically with above information
After using git-asana set <task id>, program will append task id information to the file. The file be read by the post commit hook.
    {
        "project": "<Project name>",
        "project_id": "<Project ID>",
        "workspace": "<Workspace name>",
        "workspace_id": "<Workspace ID>",
        "task": "<Task name>",
        "task_id": "<Task ID>"
    }
git-asana complete will complete the task and remove task information

To use GitAsana you have to set `ASANA_KEY` variable with value of your [API key](http://app.asana.com/-/account_api). You also have to create config file in the main directory of your repository:


To add comments automatically after every commit copy `hooks/post-commit` to `.git/hooks/post-commit` in the main directory of your repository.

Now, to use it call `git-asana` (without arguments). It will display list of your tasks in workspace and project. If you want to create a new task use `git-asana create "<task name>" <task description>`. In both cases you'll get a task id which you have to set with `. git-asana-set <task id>` (notice the dot in front of the command - it's very important).

Now just commit into git and it'll add comments to selected task on Asana automatically.

TODO
----

* Make comments format easier to change.