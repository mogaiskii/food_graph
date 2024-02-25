import datetime
import uuid

import faker
from behave import *

from api.graphql.schemas import GQAddDishDay, GQAddDishInDay
from core.interactors.dishes.interactor import create_day_with_dish

use_step_matcher("re")


fake = faker.Faker()


@given("we have a day dish data")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    dish_data_object = GQAddDishDay(
        day=datetime.date.today(), user_code=uuid.uuid4(), dish=GQAddDishInDay(name=fake.user_name())
    )
    context.day_dish_data = dish_data_object


@when("we create a day dish")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.day_dish = create_day_with_dish(session, context.day_dish_data)
    raise NotImplementedError(u'STEP: When we create a day dish')


@then("we get a day dish")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then we get a day dish')