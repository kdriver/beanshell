"""This is a module containing beanshell template text for NORSSTrack."""

imports_text = "import org.orekit.time.AbsoluteDate;\n\
import jsattrak.objects.Satellite;\n\
import org.orekit.time.TimeScalesFactory;\n\
import jsattrak.utilities.TLE;\n\n"

sat_object = 'Satellite {varName} = new Satellite(\"{sat_text}\",\"{tle_line1}\",\"{tle_line2}\");\n\
{varName}.setSatColor(new Color({colour}));\n\
NORSSTrack.AddSatelliteToList({varName});\n'
