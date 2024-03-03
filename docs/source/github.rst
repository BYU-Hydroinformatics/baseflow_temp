.. raw:: html
   :file: translate.html
   
==================
Contributors Guide
==================
Welcome to the contributors guide for our project! This guide is designed to help you get started with contributing to our open-source project. Whether you're a seasoned developer or just getting started, there are many ways you can contribute and make a difference.

This guide will walk you through the process of cloning the repository, making changes, and submitting a pull request. By following these steps, you'll be able to contribute your ideas, fixes, and improvements to the project.

We value your contributions and appreciate the time and effort you put into making our project better for everyone. Thank you for considering contributing, and we look forward to seeing your contributions!

Now, let's get started!

**Cloning the Repo**
--------------------
To contribute to our project, you'll first need to clone the repository to your local machine. Follow these steps:

1. **Fork the Repository**: Go to our project's GitHub page and click on the "Fork" button in the top-right corner. This creates a copy of the repository in your GitHub account.

2. **Clone Your Fork**: Open a terminal and use the `git clone` command to clone your forked repository to your local machine. Replace `<your_username>` with your GitHub username.

   .. code-block:: bash

      git clone https://github.com/<your_username>/your-repo.git

3. **Set Up Upstream**: Navigate to the directory of your cloned repository and set up an upstream remote pointing to the original repository.

   .. code-block:: bash

      cd your-repo
      git remote add upstream https://github.com/BYU-Hydroinformatics/baseflow.git

4. **Verify Remotes**: Ensure that your remotes are set up correctly by running:

   .. code-block:: bash

      git remote -v

**Submitting a Pull Request**
-----------------------------
Once you've made changes to the code or documentation, you can submit a pull request to have your contributions reviewed and merged into the main project. Here's how:

1. **Create a Branch**: Before making changes, create a new branch to work in. This keeps your changes isolated from the main codebase.

   .. code-block:: bash

      git checkout -b feature-branch

2. **Make Changes**: Make your desired changes to the code or documentation within your branch.

3. **Commit Changes**: Once you're satisfied with your changes, commit them to your branch.

   .. code-block:: bash

      git add .
      git commit -m "Your commit message here"

4. **Push Changes**: Push your changes to your forked repository on GitHub.

   .. code-block:: bash

      git push origin feature-branch

5. **Submit Pull Request**: Visit your forked repository on GitHub and click on the "New Pull Request" button. Select the branch you just pushed from the dropdown menu and provide a descriptive title and comment for your pull request.

6. **Review and Merge**: A project maintainer will review your pull request, possibly requesting changes. Once approved, your changes will be merged into the main project.


