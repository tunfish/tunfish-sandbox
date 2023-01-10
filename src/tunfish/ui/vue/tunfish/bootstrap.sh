# Define a software environment typical for the previous Node.js 14 LTS release.
export NODEJS_VERSION=14.19.1
export NPM_VERSION=6.14.15
export YARN_VERSION=1.22.18

# Setup Node.js environment defined by specific software versions.
source /dev/stdin <<<"$(curl -s https://raw.githubusercontent.com/cicerops/supernode/main/supernode)"
