from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restuarantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
	output = ''
	restaurants = session.query(Restaurant).all()
	for res in restaurants:
		output += res.name 
		output += '</br>restaurant id = '
		output += str(res.id)
		output += '</br>'
		items = session.query(MenuItem).filter_by(restaurant_id = res.id).all()
		for i in items:
			output += i.name
			output += '</br>'
		output += '</br>'
	return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant=restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	itemToBeEdited = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			itemToBeEdited.name = request.form['name']
		if request.form['price']:
			itemToBeEdited.price = request.form['price']
		if request.form['description']:
			itemToBeEdited.description = request.form['description']
		session.add(itemToBeEdited)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant = restaurant, menu = itemToBeEdited)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToBeDeleted = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToBeDeleted)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenutiem.html', menuItem = itemToBeDeleted)	

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
