WALL_THICKNESS = 2.5;
False = false;
True = true;

module tile (width=12, u=false, d=false, l=false, r=false) {
    wall_height = width;
    base_height = (width < 12) ? 3 : width * .25;

    union() {
        // base
        cube([width+(2*WALL_THICKNESS), width+(2*WALL_THICKNESS), base_height]);

        // walls
        union() {
            if (u) {
                translate([0, width+WALL_THICKNESS, base_height-1]) {
                    cube([width+(2*WALL_THICKNESS), WALL_THICKNESS, wall_height]);
                }
            }
            if (d) {
                translate([0,0,base_height-1]) {
                    cube([width+(2*WALL_THICKNESS), WALL_THICKNESS, wall_height]);
                }
            }
            if (l) {
                translate([0,0,base_height-1]) {
                    cube([WALL_THICKNESS, width+(2*WALL_THICKNESS), wall_height]);
                }
            }
            if (r) {
                translate([width+WALL_THICKNESS, 0, base_height-1]) {
                    cube([WALL_THICKNESS, width+(2*WALL_THICKNESS), wall_height]);
                }
            }
            if (!u) {
                if (!r) {
                    translate([width+WALL_THICKNESS, width+WALL_THICKNESS, base_height-1]) {
                        cube([WALL_THICKNESS, WALL_THICKNESS, wall_height]);
                    }
                }
                if (!l) {
                    translate([0, width+WALL_THICKNESS, base_height-1]) {
                        cube([WALL_THICKNESS, WALL_THICKNESS, wall_height]);
                    }
                }
            }
            if (!d) {
                if (!r) {
                    translate([width+WALL_THICKNESS, 0, base_height-1]) {
                        cube([WALL_THICKNESS, WALL_THICKNESS, wall_height]);
                    }
                }
                if (!l) {
                    translate([0, 0, base_height-1]) {
                        cube([WALL_THICKNESS, WALL_THICKNESS, wall_height]);
                    }
                }
            }
        }
    }
}
