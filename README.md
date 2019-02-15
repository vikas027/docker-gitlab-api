# gitlab-api

This Alpine based docker image contains some script to automate stuff after installing a fresh GitLab

At the moment there are scripts to:
- Create Personal Access Token

## Use

    docker run -it --rm \
    -e GITLAB_URL=http://gitlab.company.tld \
    -e GITLAB_ADMIN_USER=root \
    -e GITLAB_ADMIN_PASSWD=toor \
    egeneralov/docker-gitlab-api

