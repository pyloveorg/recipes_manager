#!/usr/bin/env python
# encoding: utf-8
from flask import request, redirect, flash, url_for, render_template
from main import app, db
from models import Recipe, Vote
from flask_login import current_user,  login_required
from forms import RecipeForm, VoteForm, SearchForm
from sqlalchemy import or_

@app.route('/all_recipes', methods=['GET'])
def all_recipes():
    recipes = Recipe.query.filter_by(status='Public').order_by(Recipe.id.desc()).all()
    return render_template('recipes/all_recipes.html', recipes=recipes)


@app.route('/my_recipes', methods=['GET'])
@login_required
def my_recipes():
    recipes = Recipe.query.filter_by(user=current_user).order_by(Recipe.id.desc()).all()
    return render_template('recipes/my_recipes.html', recipes=recipes)

@app.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm(request.form)
    if request.method == 'GET':
        return render_template('recipes/new.html', form=form)
    if form.validate():
        # https://stackoverflow.com/questions/33429510/wtforms-selectfield-not-properly-coercing-for-booleans fuck
        if form.status.data == '':
            form.status.data = False
        recipe = Recipe(
            title=form.title.data,
            ingredients=form.ingredients.data,
            time_needed=form.time_needed.data,
            steps=form.steps.data,
            status=form.status.data,
            user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added successfully', 'success')
        return redirect(url_for('show_recipe', recipe_id=recipe.id))

    flash('There are some problems here', 'danger')
    return render_template('recipes/new.html', form=form)

@app.route('/recipe/<recipe_id>', methods=['GET'])
def show_recipe(recipe_id):
    # TODO: check if the user can view this particular recipe -
    # is public or recipe.user_id=current_user.id
    recipe = Recipe.query.get(recipe_id)
    vote = Vote.query.filter_by(recipe_id=recipe.id, user_id=current_user.id).first()
    form = VoteForm()
    if vote:
        form.value.data = str(vote.value)
    return render_template('recipes/show.html', recipe=recipe, form=form)

@app.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    form = RecipeForm(request.form)
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    if request.method == 'POST' and form.validate():
        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data
        recipe.time_needed = form.time_needed.data
        recipe.steps = form.steps.data
        recipe.status = form.status.data
        db.session.commit()
        flash('Recipe edited successfully', 'success')
        return redirect(url_for('my_recipes'))
    # I need to set the values for ingredients and steps, because they're from textarea, and that
    # doesn't support value for field.
    form.ingredients.data = recipe.ingredients
    form.steps.data = recipe.steps
    return render_template('recipes/edit.html', form=form, recipe=recipe)

@app.route('/recipe/<recipe_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_recipe(recipe_id):
    # TODO: add a check for recipe.user_id = current_user.id
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    db.session.delete(recipe)
    db.session.commit()
    flash('Deleted recipe successfully', 'success')
    return redirect(url_for('my_recipes'))

@app.route('/vote/<int:recipe_id>', methods=['POST'])
@login_required
def vote(recipe_id):
    form = VoteForm(request.form)
    if request.method == 'POST' and form.validate():
        
        vote = Vote.query.filter_by(
            recipe_id=recipe_id,
            user_id=current_user.id
        ).first()
        if vote:
            vote.value = int(request.form['value'])
        else:
            vote = Vote(
                value=int(request.form['value']),
                user_id=current_user.id,
                recipe_id=recipe_id)
        db.session.add(vote)
        db.session.commit()
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe.calculate_average()
        db.session.add(recipe)
        db.session.commit()

        flash('Vote added successfully', 'success')
        return redirect(url_for('show_recipe', recipe_id=recipe_id))

    flash('Error: You can\'t give an empty or out of range vote', 'danger')
    return redirect(url_for('show_recipe', recipe_id=recipe_id))

@app.context_processor
def inject_searchform():
    return dict(searchform=SearchForm(request.form))

@app.route('/search', methods=['GET','POST'])
def search():
    searchform = SearchForm(request.form)
    if request.method == 'POST' and searchform.validate():
        return redirect((url_for('search_results', query=searchform.search.data)))
    flash('You didn\'t input any query, showing you all recipes instead', 'info')
    return redirect((url_for('all_recipes')))

@app.route('/search_results/<query>', methods=['GET'])
def search_results(query):
    results = Recipe.query\
        .filter(or_(Recipe.status == 'Public', Recipe.user_id == current_user.get_id()))\
        .filter(Recipe.title.contains(query))
    if results.count() > 0 :
        return render_template('search.html', query=query, recipes=results)
    elif results.count() == 0:
        return render_template('search.html', query=query, recipes=results)
    flash('Something went wrong, showing you all recipes instead', 'info')
    return render_template('search.html', query=query, recipes=results)
