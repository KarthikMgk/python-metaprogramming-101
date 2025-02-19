# Normal Approach

class Point2D:

    __slots__ = ('_x', '_y',)

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    
    def __str__(self):
        return f"({self.x},{self.y})"
    
    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"
    
    def __hash__(self):
        return hash(self.x, self.y)

    def __eq__(self, value):
        if not isinstance(value, Point2D):
            raise ValueError(f"{value} must of type {type(Point2D)}")
        return self.x == value.x and self.y == value.y
    


# p1 = Point2D(1,1)
# p2 = Point2D(1,1)

# print(p1, " is p1")
# print(p2, " is p2")

# print(p1 == p2)

class Point3D:
    __slots__ = ('_x', '_y', '_z')

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        return f"Point3D({self.x}, {self.y}, {self.z})"
    
    def __eq__(self, value):
        if not isinstance(value, Point3D):
            raise ValueError(f"{value} must be of type {type(value)}")
        return self.x == value.x and self.y == value.y and self.z == value.z
    
    def __hash__(self):
        return hash(self.x, self.y, self.z)
    


# p1 = Point3D(1,1,1)
# p2 = Point3D(1,1,1)

# print(p1)
# print(p2)

# print(p1 == p2)


# The above 2 classes has a lot of redundant code which can be cleaned with metaprogramming


#below is the metaclass

class SlottedStruct(type):
    
    def __new__(mcls, class_name, class_bases, class_dict):
        cls_object = super().__new__(mcls, class_name, class_bases, class_dict)

        # setup the slots
        slots_list = ["_"+item for item in cls_object._fields]
        setattr(cls_object, '__slots__', slots_list)

        #create read-only property for the fields
        for field in cls_object._fields:
            slot = f"_{field}"
            setattr(cls_object, field, property(
                fget=lambda self, attrib=slot: getattr(self, attrib)))

        #add the __eq__ method
        def eq(self, other):
            if not isinstance(other, cls_object):
                raise ValueError(f"{other} must be of type {type(cls_object)}")
            self_field_values = [getattr(self, field) for field in cls_object._fields]
            other_field_values = [getattr(other, field) for field in cls_object._fields]
            return self_field_values == other_field_values
        setattr(cls_object, '__eq__', eq)

        #add the __hash__ method
        def hash_(self):
            field_values = [getattr(self, field) for field in self._fields]
            return hash(tuple(field_values))
        setattr(cls_object, '__hash__', hash_)

        #add the __str__ method
        def str_(self):
            field_values = [getattr(self, field) for field in self._fields]
            field_values_joined = ",".join(map(str, field_values))
            return f"{cls_object.__name__}({field_values_joined})"
        setattr(cls_object, '__str__', str_)

        #add the __repr__ method
        def repr_(self):
            field_values = [getattr(self, field) for field in self._fields]
            field_key_values = {f"{key}={value}" for key, value in zip(cls_object._fields, field_values)}
            field_key_values_str = ', '.join(field_key_values_str)
            return f'{cls_object.__name__}({field_key_values_str})'
        setattr(cls_object, '__repr__', repr_)

        return cls_object
    

class Point2D(metaclass=SlottedStruct):
    _fields = ['x', 'y']

    def __init__(self, x, y):
        self._x = x
        self._y = y


class Point3D:
    _fields = ['x', 'y', 'z']

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

p1 = Point2D(1,1)
print(p1)