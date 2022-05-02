CREATE TABLE dog (
    dog_id INT PRIMARY KEY,
    name VARCHAR(30),
    breed VARCHAR(30),
    owner INT,
    food_info INT,
);

CREATE TABLE dog_owner (
    human_id INT PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    owner_of INT,
    FOREIGN KEY(owner_of) REFERENCES dog(dog_id) ON DELETE SET NULL
);

ALTER TABLE dog
ADD FOREIGN KEY(owner) REFERENCES dog_owner(human_id) ON DELETE SET NULL;

CREATE TABLE dog_food (
    brand_of_food VARCHAR(20) PRIMARY KEY,
    serving_size DECIMAL(3, 2),
    frequency_per_day INT,
);

ALTER TABLE dog
ADD FOREIGN KEY(food_info) REFERENCES dog_food(brand_of_food) ON DELETE SET NULL;