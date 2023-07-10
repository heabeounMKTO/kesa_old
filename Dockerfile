FROM localhost:5000/detectbase
WORKDIR /home
COPY ./kesa-data-api ./
EXPOSE 6969
CMD ["waitress-serve", "--port=6969", "--threads=1", "--call", "deploy:create_app"]