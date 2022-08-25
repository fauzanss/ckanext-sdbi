from collections import OrderedDict
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def most_recent_datasets(num=3):
        datasets = toolkit.get_action('package_search')({}, {'sort': 'metadata_modified desc',
                                                        'fq': 'private:false',
                                                        'rows': num})
        return datasets.get('results', [])

def dataset_count():
    """Return a count of all datasets"""

    result = toolkit.get_action('package_search')({}, {'rows': 1})
    return result['count']

def groups():
    """Return a list of groups"""

    return toolkit.get_action('group_list')({}, {'all_fields': True})

def package_showcase_list(context):
    return toolkit.get_action('ckanext_package_showcase_list')({}, {'package_id': context.pkg_dict['id']})

def ckan_site_url():
    return config.get('ckan.site_url', '').rstrip('/')

class SDBIPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'sdbi')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):

        if package_type != 'dataset':
            return facets_dict

        return OrderedDict([('kategori', 'Kategori'),
                            #('groups', 'Grup'),
                            ('organization', 'Walidata'),
                            #('vocab_category_all', 'Topic Categories'),
                            #('metadata_type', 'Dataset Type'),
                            #('tags', 'Tagging'),
                            ('res_format', 'Format'),
                            #('organization_type', 'Organization Types'),
                            #('publisher', 'Publishers'),
                            #('extras_progress', 'Progress'),
                            ])

    def organization_facets(self, facets_dict, organization_type, package_type):

        if not package_type:
            return OrderedDict([('organization', 'Walidata'),
                                ('kategori', 'Kategori'),
                                #('groups', 'Grup'),
                                #('organization', 'Instansi'),
                                #('vocab_category_all', 'Topic Categories'),
                                #('metadata_type', 'Dataset Type'),
                                #('tags', 'Tagging'),
                                ('res_format', 'Format'),
                                #('harvest_source_title', 'Harvest Source'),
                                #('capacity', 'Visibility'),
                                #('dataset_type', 'Resource Type'),
                                #('publisher', 'Publishers'),
                                ])
        else:
            return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):

        # get the categories key
        group_id = plugins.toolkit.c.group_dict['id']
        key = 'vocab___category_tag_%s' % group_id
        if not package_type:
            return OrderedDict([('kategori', 'Kategori'),
                                #('groups', 'Grup'),
                                ('organization', 'Walidata'),
                                #('metadata_type', 'Dataset Type'),
                                #('organization_type', 'Organization Types'),
                                #('tags', 'Tagging'),
                                ('res_format', 'Format'),
                                #(key, 'Categories'),
                                #('publisher', 'Publisher'),
                                ])
        else:
            return facets_dict

    def get_helpers(self):
        """Register sdbi_theme_* helper functions"""

        return {'sdbi_theme_most_recent_datasets': most_recent_datasets,
                'sdbi_theme_dataset_count': dataset_count,
                'sdbi_theme_groups': groups,
                'ckan_site_url': ckan_site_url,
                'package_showcase_list': package_showcase_list}
