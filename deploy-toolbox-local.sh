export OS="darwin/arm64"  #"linux/amd64" # one of linux/amd64, darwin/arm64, darwin/amd64, or windows/amd64
export VERSION=0.10.0 # see releases page for other versions: https://github.com/googleapis/genai-toolbox/releases
curl -O https://storage.googleapis.com/genai-toolbox/v$VERSION/$OS/toolbox

chmod +x toolbox

./toolbox --tools-file "tools.yaml" #you may need to run this a different port if running multiple toolbox servers locally



