main:
	cargo fmt;
	cargo run --release 0.50 0.28 0.00 0.00 0.00 0.00 0.22 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00;

run:
	cd DifferentialEvolution;
	python main.py
