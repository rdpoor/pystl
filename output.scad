difference() {
	union() {
		cylinder($fn = 64, center = true, d = 30.0, h = 10.0);
		rotate(a = [0, 0, 90]) {
			union() {
				translate(v = [20.0, 0, 0]) {
					cube(center = true, size = [40, 10.0, 10.0]);
				}
				translate(v = [40, 0, 0]) {
					rotate(a = [90, 0, 0]) {
						cylinder($fn = 64, center = true, d = 10.0, h = 10.0);
					}
				}
			}
		}
		rotate(a = [0, 0, 180]) {
			translate(v = [0, 4, 0]) {
				union() {
					translate(v = [15.0, 0, 0]) {
						cube(center = true, size = [30.0, 10.0, 10.0]);
					}
					translate(v = [30.0, 0, 0]) {
						rotate(a = [90, 0, 0]) {
							cylinder($fn = 64, center = true, d = 10.0, h = 10.0);
						}
					}
				}
			}
		}
	}
	union() {
		cylinder($fn = 64, center = true, d = 20.0, h = 10.01);
		rotate(a = [0, 0, 90]) {
			union() {
				translate(v = [20.0, 0, 0]) {
					cube(center = true, size = [45.0, 1, 10.01]);
				}
				translate(v = [40, 0, 0]) {
					rotate(a = [90, 0, 0]) {
						union() {
							cylinder($fn = 64, center = true, d = 4, h = 10.01);
							cube(center = true, size = [10.01, 10.01, 1]);
						}
					}
				}
			}
		}
		rotate(a = [0, 0, 180]) {
			translate(v = [0, 4, 0]) {
				union() {
					translate(v = [15.0, 0, 0]) {
						cube(center = true, size = [35.0, 1, 10.01]);
					}
					translate(v = [30.0, 0, 0]) {
						rotate(a = [90, 0, 0]) {
							union() {
								cylinder($fn = 64, center = true, d = 4, h = 10.01);
								cube(center = true, size = [10.01, 10.01, 1]);
							}
						}
					}
				}
			}
		}
	}
}
