from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        page = None
        status = None
        try:
            page = request.args.get('page')
        except:
            pass
        try:
            status = request.args.get('status')
        except:
            pass
        if page is not None and status is None:
            movies = movie_service.get_twenty(int(page))
        elif status is not None and page is None:
            movies = movie_service.get_newest()
        elif page is not None and status is not None:
            movies = movie_service.get_twenty_newest(int(page))
        else:
            movies = movie_service.get_all()

        return MovieSchema(many=True).dump(movies), 200

    def post(self):
        req_json = request.json
        ent = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{ent.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        movie = movie_service.get_one(bid)
        return MovieSchema(many=True).dump(movie), 200

    def put(self, bid):
        req_json = request.json
        req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    def patch(self, bid):
        req_json = request.json
        req_json["id"] = bid
        movie_service.partially_update(req_json)
        return "", 204

    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204
