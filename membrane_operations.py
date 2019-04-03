import requests

def transform(state, aspect_name, new_value, port):

	#assign new value
	state['aspects'][aspect_name] = new_value

	#send to all siblings, parents, and children
	active_siblings 	= state['active_siblings']
	parents 			= state['parents']
	children 			= state['children']
	payload				= state['aspects']
	for url in active_siblings + children + parents:
		r = requests.post(url + 'service_coordination/transform', json=payload, data=str(port))
		if not r:
			print("Transform broadcast not sent to {}".format(url))

	return state

def divide(state, number_of_additions, port):

	siblings_to_add 	= []
	for sib in state['inactive_siblings'][:number_of_additions]:
		siblings_to_add.append(sib)
	
	payload = state
	# print(payload)
	for s_url in siblings_to_add:
		r = requests.post(s_url + 'service_coordination/divide', json=payload, data=str(port))
		if r:
			state['inactive_siblings'].remove(s_url)
			state['active_siblings'] += s_url

	#send to all children and parents
	children			= state['children']
	parents				= state['parents']
	payload				= {'active_siblings':state['active_siblings']}

	print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2')
	print(children)
	print(parents)
	print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

	
	for url in children + parents:
		r = requests.post(url + 'service_coordination/divide', json=payload, data=str(port))
		if not r:
			print("Transform broadcast not sent to {}".format(url))

	return state

def merge(state, number_of_deletions, port):

	siblings_to_del		= []
	for sib in state['active_siblings'][:number_of_deletions]:
		siblings_to_del.append(sib)

	for s_url in siblings_to_del:
		r = requests.get(s_url + 'service_coordination/merge')
		if not r:
			print("Merge broadcast was not sent to {}".format(s_url))
		state['active_siblings'].remove()
		state['inactive_siblings'] += s_url

	#send to all siblings, parents and children

	payload = {'active_siblings':state['active_siblings']}
	for url in parents + siblings + children:
		r = requests.post(url + 'service_coordination/merge', json=payload, data=port)
		if not r:
			print("Transform broadcast not sent to {}".format(url))

	return state