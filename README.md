<div align="center">
  <h3 align="center">URL Shortener</h3>
</div>



<!-- GETTING STARTED -->
## Getting Started

* Prerequisites
  ```sh
  Docker
  Add environment variable URL_POSTGRES_USER root
  Add environment variable URL_POSTGRES_PASSWORD root
  ```

* Build docker images
  ```sh
  build.bat
  ```

* Run docker containers
  ```sh
  run.bat
  ```


* Create short code
  ```sh
  http://localhost:5000/urlshortner/create/<URL_PATH>/<SHORT_CODE_SIZE>
  ```

* Resolve short code
  ```sh
  http://localhost:5001/urlshortner/redirect/<SHORT_CODE>
  ```

