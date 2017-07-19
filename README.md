# interconnect_qa
Repository dedicated to test automation &amp; tool development

prerequisities - sultan 0.3.1+, proton 0.17.0+

Folder description:
examples - contains various examples that can serve as a template for further development. Currently contains only
small set of reproducers used during issue verification

selftests - unittest for developed tools, components or another different module from ./src

src/components - components serving as an integral part for interconnect_qa project. All logic is set here
src/tools - set of tools that is possible to use standalone, without any further usage of src/components

tests - all interconnect tests should be here