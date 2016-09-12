from PIL import Image

LEFT, DASH, RIGHT = (None, None, None)
UPPER, LOWER = (None, None)
def isBlack(pixel):
    """ 
    takes pixel(RGB) as input
    returns boolean value, whether it is black

    black as pixel(x,y,z) x<10 and y<10 and z<10
    otherwise non-black
    """
    x,y,z = pixel
    if x<20 and y<20 and z<20:
        return True
    else:
        return False

def isWhite(pixel):
    """ 
    takes pixel(RGB) as input
    returns boolean value, whether it is white

    black as pixel(x,y,z) x>245 and y>245 and z>245
    otherwise non-black
    """
    x,y,z = pixel
    if x>245 and y>245 and z>245:
        return True
    else:
        return False

def exploreLeftToRight(im):
    global LEFT,DASH,RIGHT
    """ 
    takes PIL Image object as input
    returns a tuple consisting of left boundary, dashed line and right boundary of the plotting
    while all these lines are lists of x coordinate
    
    e.g.
    exploreLeftToRight(im) = ([149,150],[614,615],[1079,1080])
    """
    xsize, ysize = im.size
    flag = False
    lines = []
    #find the left and right boundary
    for x in range(xsize):
    	#initialize the black points
    	black_point = 0
    	for y in range(ysize):
    		pixel = im.getpixel((x, y))
    		if isBlack(pixel):
    			#calculate the black points
    			black_point += 1
        #get the boundary line
    	if black_point > ysize/3:
    		if not flag:
    			flag = True
    			line = []
    			line.append(x)
    		else:
    			line.append(x)
    	else:
    		if flag:
    			flag = False
    			lines.append(line)
    #raise the expection
    if len(lines) != 3:
        if LEFT == None:
            raise Exception('Some Wrong with the graph '+im.filename)
        else:
            left, dash, right = LEFT,DASH,RIGHT
    else:
        left, dash, right = lines[0],lines[1],lines[2]
        LEFT,DASH,RIGHT = left, dash, right
    return (left, dash, right)

def exploreUpToDown(im):
    global UPPER,LOWER
    """ 
    takes PIL Image object as input
    returns a tuple consisting of upper boundary and lower boundary of the plotting
    while both upper and lower boundary are lists of y coordinate
    
    e.g.
    exploreUpToDown(im) = ([59,60],[539,540])
    """
    xsize, ysize = im.size
    flag = False
    lines = []
    #find the left and right boundary
    for y in range(ysize):
        #initialize the black points
        black_point = 0
        for x in range(xsize):
            pixel = im.getpixel((x, y))
            if isBlack(pixel):
                #calculate the black points
                black_point += 1
        #get the boundary line
        if black_point>ysize/3:
            if not flag:
                flag = True
                line = []
                line.append(y)
            else:
                line.append(y)
        else:
            if flag:
                flag = False
                lines.append(line)
    #raise the exception
    if len(lines) != 2:
        if UPPER == None:
            raise Exception('Some Wrong with the graph '+im.filename)
        else:
            upper, lower = UPPER, LOWER
    else:
        upper, lower = lines[0],lines[1]
        UPPER, LOWER = upper, lower
    return (upper, lower)

def isLeftNode(point, image, upper, lower):
    """
    takes(point, image, upper, lower) as input
    where point is coordinate(tuple),
          image is the Image object,
          upper is upper boundary(list of y coordinate),
          lower is lower boundary(list of y coordinate)
    returns boolean value, whether the point has left connection
    """
    r = int((lower[0]-upper[-1])*0.9)
    return any([isBlack(image.getpixel((point[0]-1,point[1]-2-i))) for i in range(r)])

def isRightNode(point, image, upper, lower):
    """
    takes(point, image, upper, lower) as input
    where point is coordinate(tuple),
          image is the Image object,
          upper is upper boundary(list of y coordinate),
          lower is lower boundary(list of y coordinate)
    returns boolean value, whether the point has right connection
    """
    r = int((lower[0]-upper[-1])*0.9)
    return any([isBlack(image.getpixel((point[0]+1,point[1]-2-i))) for i in range(r)])

def checkIntersection(im,left_boundary,right_boundary,lower,upper):
    """
    takes(im,left_boundary,right_boundary,lower,upper) as input
    where im is the Image object,
          left_boundary is x coordinate,
          right_boundary is x coordinate,
          upper is upper boundary(list of y coordinate),
          lower is lower boundary(list of y coordinate)
    returns boolean value, whether the part between left_boundary and right_boundary has specific pattern
    """
    black_points = []
    flag = False
    #check about the left part
    lower_bound = lower[0]-1
    for x in range(left_boundary+1,right_boundary):
        pixel = im.getpixel((x, lower_bound))
        if isBlack(pixel):
            if not flag:
                # get into the point
                flag = True
                black_point = []
                black_point.append(x)
            else:
                black_point.append(x)
        else:
            if flag:
                flag = False
                black_points.append(black_point)
    #now we have all the black points	
    #we need to iterate through them
    stack = []
    isPattern = False
    intersection_points = []

    for black_point in black_points:
        #print black_point,"left",isLeftNode((black_point[0],lower_bound), im, upper, lower),"right",isRightNode((black_point[-1],lower_bound), im, upper, lower)
        #left point
        if isLeftNode((black_point[0],lower_bound), im, upper, lower) and (not isRightNode((black_point[-1],lower_bound), im, upper, lower)):
            #insert into the stack
            stack.append(black_point)
        #right point
        elif (not isLeftNode((black_point[0],lower_bound), im, upper, lower)) and isRightNode((black_point[-1],lower_bound), im, upper, lower):
            #stack has left point
            if stack:
                #it is the pattern
                isPattern = True
                #pop out the left point, and add to the intersection points
                intersection_points.append((stack.pop(-1), black_point))
    return isPattern, intersection_points

def checkCenter(im, lower, upper, dash):
    """
    takes(im, lower, upper, dash) as input
    where im is the Image object,
          upper is upper boundary(list of y coordinate),
          lower is lower boundary(list of y coordinate),
          dash is dashed line(list of x coordinate)
    returns boolean value, whether the center part has specific pattern
    """
    leftPart = False
    rightPart = False

    #newly added
    threshold_len = int((lower[0] - upper[-1])/16)
    for y in range(upper[-1]+1, lower[0] - threshold_len):
    	pixel = im.getpixel((dash[0]-1, y))
    	if isBlack(pixel):
    		leftPart = True
        pixel = im.getpixel((dash[-1]+1, y))
        if isBlack(pixel):
        	rightPart = True
    return leftPart or rightPart

def calculate_intercept(left_coor, right_coor, left_boundary, right_boundary, points):
    """
    takes(left_coor, right_coor, left_boundary, right_boundary, points) as input
    where left_coor, right_coor are actual boundary coordinates of the graph,
          left_boundary, right_boundary are pixel indices
          points are intercepts with X-axis
    returns coordinates of those points
    """
    coordinates = []
    for two_point in points:
        for point in two_point:
            avg_point = (point[0]+point[-1])/2
            coordinate = left_coor + (right_coor - left_coor)*(avg_point - left_boundary)*1.0/(right_boundary - left_boundary)
            coordinates.append(round(coordinate, 1))
    return coordinates

def detect(img_path, verbose=True):
    """
    takes(img_path, verbose) as input
    where img_path is the file path of the graph,
          verbose is the mode to print specific info
    returns boolean value, whether a graph is the target graph
    """
    #extra_info to store some information
    extra_info = None
    im = Image.open(img_path)
    left,dash,right = exploreLeftToRight(im)
    upper, lower = exploreUpToDown(im)
    #check left part
    leftOK, left_intercept_points = checkIntersection(im,left[-1],dash[0],lower,upper)
    #check right part
    rightOK, right_intercept_points = checkIntersection(im,dash[-1],right[0],lower,upper)
    #check the center
    centerOK = checkCenter(im, lower, upper, dash)
    #print out the info
    if verbose:
        print img_path, "has pattern: ",leftOK and rightOK and centerOK
        print "More Info:"
        print "left:",leftOK,"\tright:",rightOK,"\tcenter:",centerOK
        if leftOK and rightOK and centerOK:
            extra_info = (calculate_intercept(-10,0,left[-1],dash[0],left_intercept_points),calculate_intercept(0,10,dash[-1],right[0],right_intercept_points))
            print "left intercepts:",extra_info[0]
            print "right intercepts:",extra_info[1]
        print "-------------------------------------------------------------"
    return leftOK and rightOK and centerOK, extra_info
