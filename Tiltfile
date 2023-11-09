# Deploy: tell Tilt what YAML to deploy
k8s_yaml(helm('deploy'), allow_duplicates=True)

# Build: tell Tilt what images to build from which directories
docker_build('islam25/webapp', '.', dockerfile='./projects/webapp/Dockerfile')
docker_build('islam25/inferengine', '.', dockerfile='./projects/inferengine/Dockerfile')

k8s_resource('webapp', port_forwards=8000)
