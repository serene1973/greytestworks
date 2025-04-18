
def pytest_runtest_makereport(item, call):
    if hasattr(item.function, "__pytest_bdd_scenario__"):
        scenario = item.function.__pytest_bdd_scenario__
        tags = scenario.tags  # List of tags, e.g., ["rally.tc123"]
        
        rally_tags = [t for t in tags if t.startswith("rally.")]
        if rally_tags:
            rally_id = rally_tags[0].split(".", 1)[1]
            print(f"Rally ID from feature file: {rally_id}")
