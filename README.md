
# I'M @ PARK


This repository contain the backend side code of im@park.


![check workflow!](https://github.com/subham73/imatpark_backend/actions/workflows/checks.yml/badge.svg)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

## Get started 🚀


## Devloper Setup 🛠️

### Prerequisites
- Git
- Docker and Docker Compose

check if the tools are installed by running the following commands in your terminal.
```shell
git --version
docker --version
docker-compose --version

```

### Configure your fork
1 - Fork this [repository](https://github.com/subham73/imatpark_backend) by clicking on the "[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo)" button at the top right of the page. This will create a copy of the project under your GitHub account.

2 - [Clone your fork](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your local disk and set the upstream to this repo. New to upstream? [Check this out](https://docs.github.com/en/github/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-for-a-fork).
```shell
git clone https://github.com/<YOUR_GITHUB_ACCOUNT>/imatpark_backend.git
cd imatpark_backend
git remote add upstream https://github.com/subham73/imatpark_backend.git
```
### Environment configuraion

In order to run the project, you will need to specify some information, which can be done using a `.env.dev` file.
Copy the default environment varible from [`.env.dev-example`](./.env.dev-example) and create a new file named `.env.dev` in the root of the project.

```shell
cp .env.dev-example .env.dev
```
This file contains all the environment variables needed to run the project. You can change the values as needed.
For starters, you can keep the default values as it is. Just add your secret key for the Django project.

#### Values you have to replace
- `SECRET_KEY` : the secret key for the Django project. You can generate one [here](https://djecrety.ir/).

### Running the project
Make sure your Docker daemon is running. You can start the daemon manually by running the app.
```shell
docker-compose --build
docker-compose up
```
and volla, the project is running on `http://localhost:8000/`.
You can access the API documentation at `http://localhost:8000/api-docs/`.

### Running the tests
To run the tests, you can use the following command.
```shell
docker-compose run --rm app sh -c "python manage.py test"
```

### Running the linter
To run the linter, for code quality you can use the following command.
```shell
docker-compose run --rm app sh -c "flake8"
```

### Submitting a Pull Request

1. **Create a New Branch**: You should not work on the `main` branch. Create a new branch with a descriptive name for the feature you are working on.
    ```shell
    git checkout -b <BRANCH_NAME>
    ```

2. **Make Changes**: After you have made the changes, add and commit them. Remember to add a meaningful commit message.
    ```shell
    git add .
    git commit -m "Your meaningful commit message"
    ```

3. **Pull Latest Changes**: Before pushing your changes, pull the latest changes from the upstream `main` branch to ensure your branch is up-to-date.
    ```shell
    git pull upstream main
    ```

4. **Resolve Conflicts**: If there are any conflicts, resolve them and commit the resolved changes.
    ```shell
    git add .
    git commit -m "Resolve merge conflicts"
    ```

5. **Push Changes**: Push the changes to your fork.
    ```shell
    git push origin <BRANCH_NAME>
    ```

6. **Run Tests and Linting**: Before creating a PR, make sure the tests are passing, and the code is formatted properly.
    ```shell
    docker-compose run --rm app sh -c "python manage.py test && flake8"
    ```

7. **Create a Pull Request**: If the tests are passing and the code is formatted properly, you can create a PR. Create a Pull Request from your fork to this repository. Make sure to add a meaningful title and description to the PR.

8. **Review and Address Feedback**: After creating the PR, reviewers may leave comments or request changes. Make sure to address their feedback promptly.

9. **Keep Your Branch Updated**: While your PR is being reviewed, keep your branch updated with the latest changes from the upstream `main` branch.
    ```shell
    git pull upstream main
    git push origin <BRANCH_NAME>
    ```
10. Congrats you did it 🎉




