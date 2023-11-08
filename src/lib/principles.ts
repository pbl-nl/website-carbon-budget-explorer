// Top colors from https://colorbrewer2.org/#type=qualitative&scheme=Set3&n=9
/*
#8dd3c7
#ffffb3
#bebada
#fb8072 to much like ndc
#80b1d3
#fdb462
#b3de69 to much like pathway
#fccde5
#d9d9d9
*/
export const principles = {
	GF: {
		label: 'Grandfathering',
		summary: 'Past emissions levels.',
		color: '#8dd3c7'
	},
	PC: {
		label: 'Per capita',
		summary: 'Population.',
		color: '#ffffb3'
	},
	PCC: {
		label: 'Per capita convergence',
		summary: 'Population with convergence in 2040.',
		color: '#bebada'
	},
	AP: {
		label: 'Ability to pay',
		summary: 'A country’s ability to pay for mitigation.',
		color: '#80b1d3'
	},
	GDR: {
		label: 'GH development rights',
		summary: 'Equalize per capita emissions across countries.',
		color: '#fdb462'
	},
	ECPC: {
		label: 'Equal cumulative per capita',
		summary: 'A country’s cumulative emissions per capita.',
		color: '#fccde5'
	}
} as const;
