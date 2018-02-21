#!/usr/bin/env python
# encoding: utf-8
from flask import request, redirect, flash, url_for, render_template
from main import app, db
from models import Recipe
from flask_login import current_user,  login_required
from forms import RecipeForm

@app.route('/', methods=['GET'])
def all_recipes():
    # TODO: only public ones!
    return render_template('recipes/all_recipes.html')

@app.route('/my_recipes', methods=['GET'])
@login_required
def my_recipes():
    # TODO: all recipes from current user
    return render_template('recipes/my_recipes.html')

@app.route('/new_recipe', methods=['GET', 'POST'])
def new_recipe():
    form = RecipeForm(request.form)
    if request.method == 'POST':
        recipe = Recipe(
            title=form.title.data,
            ingredients=form.ingredients.data,
            time_needed=form.time_needed.data,
            steps=form.steps.data,
            is_public=form.is_public.data,
            user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added successfully', 'success')
        return redirect(url_for('show_recipe', recipe_id=recipe.id))

    return render_template('recipes/new.html', form=form)

@app.route('/recipe/<recipe_id>', methods=['GET'])
def show_recipe(recipe_id):
    # TODO: check if the user can view this particular recipe -
    # is public or recipe.user_id=current_user.id
    recipe = Recipe.query.get(recipe_id)
    return render_template('recipes/show.html', recipe=recipe)

@app.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    form = RecipeForm(request.form)
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    if request.method == 'POST':
        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data
        recipe.time_needed = form.time_needed.data
        recipe.steps = form.steps.data
        recipe.is_public = form.is_public.data
        db.session.commit()
        flash('Recipe edited successfully', 'success')
        return redirect(url_for('my_recipes'))

    return render_template('recipes/edit.html', form=form, recipe=recipe)

@app.route('/recipe/<recipe_id>/delete', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    # TODO: add a check for recipe.user_id = current_user.id
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    db.session.delete(recipe)
    db.session.commit()
    flash('Deleted post successfully', 'success')
    return redirect(url_for('my_recipes'))
