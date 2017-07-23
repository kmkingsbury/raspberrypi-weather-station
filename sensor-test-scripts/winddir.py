class wind_direction(object):
    def __init__(self, adc_channel=0, config_file=None):

        config_file_path = os.path.join(os.path.dirname(__file__), config_file)

        with open(config_file_path, "r") as f:
            self.config = json.load(f)

        vin = self.config["vin"]
        vdivider = self.config["vdivider"]

        for dir in self.config["directions"]:
            dir["vout"] = self.calculate_vout(vdivider, dir["ohms"], vin)
            dir["adc"] = round(self.adc.max * (dir["vout"] / self.adc.vref))

        sorted_by_adc = sorted(self.config["directions"], key=lambda x: x["adc"])

        for index, dir in enumerate(sorted_by_adc):
            if index > 0:
                below = sorted_by_adc[index - 1]
                delta = (dir["adc"] - below["adc"]) / 2.0
                dir["adcmin"] = dir["adc"] - delta + 1
            else:
                dir["adcmin"] = 1

            if index < (len(sorted_by_adc) - 1):
                above = sorted_by_adc[index + 1]
                delta = (above["adc"] - dir["adc"]) / 2.0
                dir["adcmax"] = dir["adc"] + delta
            else:
                dir["adcmax"] = self.adc.max - 1

    def calculate_vout(self, ra, rb, vin):  # Ohm's law resistive divider calculation
        return (float(rb) / float(ra + rb)) * float(vin)

    def get_dir(self, adc_value):
        angle = None

        for dir in self.config["directions"]:
            if (adc_value > 0 and
            adc_value >= dir["adcmin"] and
            adc_value <= dir["adcmax"] and
            adc_value < self.adc.max):
                angle = dir["angle"]
                break

        return angle

    def get_average(self, angles):
        """
        Consider the following three angles as an example: 10, 20, and 30
        degrees. Intuitively, calculating the mean would involve adding these
        three angles together and dividing by 3, in this case indeed resulting
        in a correct mean angle of 20 degrees. By rotating this system
        anticlockwise through 15 degrees the three angles become 355 degrees,
        5 degrees and 15 degrees. The naive mean is now 125 degrees, which is
        the wrong answer, as it should be 5 degrees.
        """

        # http://en.wikipedia.org/wiki/Directional_statistics

        sin_sum = 0.0
        cos_sum = 0.0

        for angle in angles:
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        flen = float(len(angles))
        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average

    def get_value(self, length=5):
        data = []
        print("Measuring wind direction for %d seconds..." % length)
        start_time = time.time()

        while time.time() - start_time <= length:
            adc_value = self.adc.read(self.adc_channel)
            direction = self.get_dir(adc_value)
            if direction is not None:  # keep only good measurements
                data.append(direction)
            else:
                print("Could not determine wind direction for ADC reading: %s" % adc_value)

        return self.get_average(data)
