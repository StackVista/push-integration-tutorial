from stackstate_checks.base import AgentCheck, ConfigurationError, TopologyInstance
import random

class ExampleCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    # Returns the instance check key that uniquely identifies this check instance
    # This instance of the check is identified by the type (`example`) and the URL.
    # Note that this configuration must match the configuration of the Cusomt Synchronization StackPack in StackState.
    def get_instance_key(self, instance):
        if 'url' not in instance:
            raise ConfigurationError('Missing url in agent check instance configuration.')

        instance_url = instance['url']

        return TopologyInstance("example", instance_url)

    def check(self, instance):
        self.log.debug("starting check for instance: %s" % instance)

        # start a topology snapshot
        # a topology snapshot represents the complete state of (part of) the IT landscape
        # it completely replaces the previous state of the landscape
        # this means that components that are no longer present in the current snapshot will be removed
        self.start_snapshot()

        # send a component to StackState
        self.component("host_fqdn", "host", {
            # define the name of the component that is shown in the StackState GUI
            "name": "a-host",

            # define the component domain, by default shown horizontally on the topology grid
            "domain": "Example",

            # define the component layer, by default shown vertically on the topology grid
            "layer": "Hosts",

            # define the component environment
            "environment": "Production",

            # define additional identifiers for this component
            # these identifiers enable the component to merge with other components
            # the format below is used by the agent StackPack for hosts
            # if the agent discovers the same host and their FQDN's match, StackState will merge the components into a single component
            "identifiers": ["urn:host:/host_fqdn"],

            # define labels (aka tags) for this component
            # these labels can be used to find the component using topology filters
            "labels": ["example", "host:a_host"]
        })

        self.component("application_id_1", "application", {
            "name": "some-application-1",
            "domain": "Example",
            "layer": "Applications",
            "identifiers": ["urn:process:/some_application_1"],
            "labels": ["example","application:some_application_1", "hosted_on:a-host"],
            "environment": "Production",
            "version": "0.2.0"
        })

        self.component("application_id_2", "application", {
            "name": "some-application-2",
            "domain": "Example",
            "layer": "Applications",
            "identifiers": ["urn:process:/some_application_2"],
            "labels": ["example","application:some_application_2", "hosted_on:a-host"],
            "environment": "Production",
            "version": "3.1.2"
        })

        # send a relation between two components to StackState
        # the relation is directed from the first component to the second
        # in this case, the `application_id_1` component depends on the `host_fqdn` component
        self.relation("application_id_1", "host_fqdn", "IS_HOSTED_ON", {})
        self.relation("application_id_2", "host_fqdn", "IS_HOSTED_ON", {})

        # complete the snapshot
        self.stop_snapshot()

        # send a metric to StackState
        self.gauge("example.gauge", random.random() * 1000, ["related:application_id_1"])
        self.gauge("example.gauge", random.random() * 1000, ["related:application_id_2"])

        self.log.debug("successfully ran check for instance: %s" % instance)
