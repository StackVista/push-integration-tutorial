docker run -v `pwd`:/etc/stackstate-agent -e STS_API_KEY -e STS_STS_URL --env DOCKER_STS_AGENT=false stackstate/stackstate-agent-2:latest
