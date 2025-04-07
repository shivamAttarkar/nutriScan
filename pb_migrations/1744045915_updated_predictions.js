/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2121703314")

  // add field
  collection.fields.addAt(5, new Field({
    "hidden": false,
    "id": "select1164694065",
    "maxSelect": 1,
    "name": "classification",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "Healthy",
      "Moderately Healthy",
      "Unhealthy"
    ]
  }))

  // update field
  collection.fields.addAt(3, new Field({
    "hidden": false,
    "id": "json891901793",
    "maxSize": 0,
    "name": "classified_ingredients",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // update field
  collection.fields.addAt(4, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text2703623258",
    "max": 0,
    "min": 0,
    "name": "extracted_text",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2121703314")

  // remove field
  collection.fields.removeById("select1164694065")

  // update field
  collection.fields.addAt(3, new Field({
    "hidden": false,
    "id": "json891901793",
    "maxSize": 0,
    "name": "classifiedIngredients",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // update field
  collection.fields.addAt(4, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text2703623258",
    "max": 0,
    "min": 0,
    "name": "extractedIngredients",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
})
