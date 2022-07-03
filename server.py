import json

from aiohttp import web
from gino import Gino

PG_DSN = 'postgres://admin:admin@127.0.0.1:5432/aiohttp_hw'

app = web.Application()
db = Gino()


class HTTPException(web.HTTPClientError):

    def __init__(self, *args, error='', **kwargs):
        kwargs['text'] = json.dumps({'error': error})
        super().__init__(*args, **kwargs, content_type='application/json')


class NotFound(HTTPException):
    status_code = 404


# Create model for ORM
class Adverts(db.Model):
    __tablename__ = 'adverts'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), server_default='now()')
    owner_name = db.Column(db.Text(), nullable=False)

    _idx1 = db.Index('app_adverts_name', 'name')


async def init_orm(app):
    print('App start')
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('App closed')


class AdvertsView(web.View):

    async def get(self):
        advert_id = int(self.request.match_info['id'])
        advert = await Adverts.get(advert_id)
        if advert is None:
            raise NotFound(error="user does not exist")
        return web.json_response({
            'name': advert.name,
            'description': advert.description,
            'create_time': advert.date.isoformat(),
            'owner': advert.owner_name
        })

    async def post(self):
        json_data = await self.request.json()
        new_advert = await Adverts.create(
            name=json_data['name'],
            description=json_data['description'],
            owner_name=json_data['owner_name'])

        return web.json_response({
            'id': new_advert.id,
            'name': new_advert.name,
            'description': new_advert.description,
            'time': new_advert.date.isoformat(),
            'owner': new_advert.owner_name
        })

    async def put(self):
        json_data = await self.request.json()
        advert_id = int(self.request.match_info['id'])
        advert_update = await Adverts.query.where(Adverts.id == advert_id).gino.first()
        print(advert_update)
        await advert_update.update(
            name=json_data['name'],
            description=json_data['description'],
            owner_name=json_data['owner_name']
        ).apply()

        if advert_update is None:
            raise NotFound(error="user does not exist")

        return web.json_response({
            'name': advert_update.name,
            'description': advert_update.description,
            'create_time': advert_update.date.isoformat(),
            'owner': advert_update.owner_name
        })

    async def delete(self):
        advert_id = int(self.request.match_info['id'])
        advert_del = await Adverts.delete.where(Adverts.id == advert_id).gino.status()

        if advert_del is None:
            raise NotFound(error="user does not exist")

        return web.json_response({advert_id: 'delete'})


app.router.add_route('POST', '/advert/', AdvertsView)
app.router.add_route('GET', '/advert/{id:\d+}', AdvertsView)
app.router.add_route('PUT', '/advert/{id:\d+}', AdvertsView)
app.router.add_route('DELETE', '/advert/{id:\d+}', AdvertsView)
app.cleanup_ctx.append(init_orm)

web.run_app(app)
