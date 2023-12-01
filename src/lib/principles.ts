// Top colors from https://venngage.com/tools/accessible-color-palette-generator

export const principles = {
	GF: {
		label: 'Grandfathering',
		summary: 'Continuity. Based on current emission levels',
		color: '#0a3dda'
	},
	PC: {
		label: 'Per capita',
		summary: 'Equality. Based on current population levels.',
		color: '#8b10c8'
	},
	PCC: {
		label: 'Per capita convergence',
		summary: 'Continuity and equality. Converging from grandfathering to per capita in 2050.',
		color: '#d01581'
	},
	AP: {
		label: 'Ability to pay',
		summary: 'Capability. Based on GDP per capita',
		color: '#00afaf'
	},
	GDR: {
		label: 'GH development rights',
		summary:
			'Capability + Responsibility. Based on GDP per capita and a responsibility-capability index.',
		color: '#dc9a00'
	},
	ECPC: {
		label: 'Equal cumulative per capita',
		summary:
			'Responsibility + Equality. Based on historical emissions and the past and future per capita share.',
		color: '#ae6600'
	}
} as const;
