from aospdtgen.proprietary_files.section import Section, register_section

class AuthsecretSection(Section):
	name = "Authsecret"
	interfaces = [
		"android.hardware.authsecret",
	]

register_section(AuthsecretSection)
