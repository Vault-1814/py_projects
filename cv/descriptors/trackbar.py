import cv2


class Filter:
    def __init__(self, title, min, max, value):
        self.title = title
        self.min = min
        self.max = max
        self.value = value


class Trackbar:
    def __init__(self, *filters):
        self.winName = "Trackbars"
        self.all_filters = []
        self.addFilters(filters)
        self.setup_trackbars(self.all_filters)

    def addFilter(self, filter):
        self.all_filters.append(filter)

    def addFilters(self, *filters):
        for f in filters[0]:
            print(f.title)
            self.all_filters.append(f)

    def callback(self, value):
        pass

    def setup_trackbars(self, range_filter):
        cv2.namedWindow(self.winName, 0)
        for j in range_filter:
            for i in ["MIN"]:
                v = j.min if i == "MIN" else j.max
                cv2.createTrackbar("%s_%s" % (j.title, i), self.winName, int(j.value), j.max, self.callback)

    def get_trackbar_values(self):
        values = []
        for i in ["MIN"]:
            for j in self.all_filters:
                v = cv2.getTrackbarPos("%s_%s" % (j.title, i), self.winName)
                values.append(v)
        return values

    def getTrackbarValue(self, filter_title):
        for f in self.all_filters:
            if f.title == filter_title:
                return cv2.getTrackbarPos(f.title, self.winName)
