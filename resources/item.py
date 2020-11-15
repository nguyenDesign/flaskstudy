from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from model.itemmodel import ItemModel


class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except Exception as e:
            return {f"message": f"An error occurred inserting the item. {e}"}
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return f"{name} has been deleted"
        else:
            return f"{name} is not existed"

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.save_to_db()
            return item.json()
        else:
            return f"Cannot find {name}"


class ItemList(Resource):
    @jwt_required
    def get(self):
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': [x.json() for x in ItemModel.query.all()]}