from django_seed import Seed
from listings.models import Listing, Category

seeder = Seed.seeder()

seeder.add_entity(Listing, 50)  # Seed 10 User objects
seeder.add_entity(Category, 5)  # Commented out to exclude Post objects

inserted_pks = seeder.execute()