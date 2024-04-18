# Description

This is an attempt at converting [matterport-dl](https://github.com/rebane2001/matterport-dl) to a Flask app so it can be served via the Flask HTTP server, instead of relying on the Python HTTP server which is how it's currently implemented (see this [gist](https://gist.github.com/jdstone/875ebdf3f3e5e88c44efb8ea0422d09d)). However, depending on future research and decisions, this project may turn into a Docker container with the content being served by Nginx. This might end up being the best solution. We'll see...

I did create a Docker container, which is hosted on my [Docker Hub](https://hub.docker.com/u/jdstone) (though the repo is currently private -- see screenshot below) with this matterport-dl software that serves a 3D tour of a home, but in it's current implemention, it relies on the internal Python [HTTP server](https://docs.python.org/3/library/http.server.html). This is not a secure or good practice to rely on the internal Pythong HTTP server for production purposes, hence why I'm re-working this.

![Screenshot of my matterport-dl Docker continer hosted on Docker Hub.](https://raw.githubusercontent.com/jdstone/matterport-dl-flask/main/matterport-dl_dockerhub_container.png)
