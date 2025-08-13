from fastapi.testclient import TestClient

from birds_store.main import app


def run():
	client = TestClient(app)

	# Health
	r = client.get("/health")
	assert r.status_code == 200, r.text
	print("health:", r.json())

	# Create
	payload = {
		"name": "Parrot",
		"species": "Psittaciformes",
		"price": 99.99,
		"in_stock": 5,
		"description": "Colorful",
	}
	r = client.post("/birds", json=payload)
	assert r.status_code == 201, r.text
	bird = r.json()
	print("created:", bird)
	bird_id = bird["id"]

	# List
	r = client.get("/birds")
	assert r.status_code == 200, r.text
	print("list:", r.json())

	# Get by id
	r = client.get(f"/birds/{bird_id}")
	assert r.status_code == 200, r.text
	print("get:", r.json())

	# Update
	r = client.patch(f"/birds/{bird_id}", json={"in_stock": 7, "price": 109.5})
	assert r.status_code == 200, r.text
	print("updated:", r.json())

	# Delete
	r = client.delete(f"/birds/{bird_id}")
	assert r.status_code == 204, r.text
	print("deleted id:", bird_id)


if __name__ == "__main__":
	run()