$fn = 60;

difference()
{
    cylinder(10, 50, 50);

    translate([0,0,10]) sphere(10);

    translate([15,-5,9.5]) linear_extrude(1) text("Test");
    
    translate([-5,20,5]) cube([10, 20, 10]);
    
    translate([0,-40,10]) rotate([-90,0,0]) cylinder(20, 5, 5);
}
