#########################################################################
#
#   Copyright 2018 VMware, Inc.  All rights reserved. VMware Confidential
#
#########################################################################
from argparse import ArgumentParser
from codecs import open as codecOpen
from contextlib import closing
from csv import DictReader
from json import dump
from StringIO import StringIO

_EAM_EXT_KEY = 'com.vmware.vim.eam'

_EXT_KEY = 'EXT_ID'
_KEY = 'DATA_KEY'
_VALUE = 'DATA_VALUE'

_CSV_FIELDS = [_EXT_KEY, _KEY, _VALUE, 'SURR_KEY']

_GLOBAL_NAME = 'global:name'
_GLOBAL_NAME_REF = _GLOBAL_NAME + '.ref.'
_GLOBAL_NAME_CNT = _GLOBAL_NAME + '.count.'

_AGENCY_IDX_PREFIX = '::EsxAgentManager:EsxAgentManager:agency['
_AGENCY_IDX_SUFFIX = ']'
_AGENCY_IS_EXT = '{}:ownerIsExtension'
_AGENCY_GOAL_STATE = '{}:goalState'
_AGENCY_EXT_KEY = '{}:extensionKey'
_AGENCY_CONFIG = '{}:config'
_AGENCY_SOL_NAME = '{}:solutionName'

_AGENT_IDX_PREFIX = '{}:agent['
_AGENT_IDX_SUFFIX = '].id'
_AGENT_GOAL_STATE = '{}:goalState'
_AGENT_NIC_TO_IP = '{}:controlNicKeyToIp'
_AGENT_HOST = '{}:host'
_AGENT_WAS_UPGRADING = '{}:wasUpgrading'
_AGENT_IS_UPGRADING = '{}:isUpgrading'
_AGENT_BASE_OVF_ENV = '{}:baseOvfEnvironment'
_AGENT_REBOOT_AFTER = '{}:rebootHostAfterVibUninstall'
_AGENT_CONFIG = '{}:config'

# OUTPUT
_JSON_COUNTERS = 'NAMED COUNTERS'
_JSON_COUNTER_REFS = 'REFERENCES'
_JSON_COUNTER_VALUE = 'VALUE'

_JSON_AGENCIES = 'AGENCIES'
_JSON_AGENCY_IS_EXT = 'OWNER IS EXTENSION'
_JSON_AGENCY_GOAL_STATE = 'GOAL STATE'
_JSON_AGENCY_EXT_KEY = 'EXTENSION KEY'
_JSON_AGENCY_CONFIG = 'CONFIG'
_JSON_AGENCY_SOL_NAME = 'SOLUTION NAME'
_JSON_AGENTS = 'AGENTS'

_JSON_AGENT_GOAL_STATE = 'GOAL STATE'
_JSON_AGENT_NIC_TO_IP = 'CONTROL NIC KEY TO IP'
_JSON_AGENT_HOST = 'HOST'
_JSON_AGENT_WAS_UPGRADING = 'WAS UPGRADING'
_JSON_AGENT_IS_UPGRADING = 'IS UPGRADING'
_JSON_AGENT_BASE_OVF_ENV = 'BASE OVF ENVIRONMENT'
_JSON_AGENT_REBOOT_AFTER = 'REBOOT AFTER UNINSTALL'
_JSON_AGENT_CONFIG = 'CONFIG'

_JSON_DB_INDEX = 'DB INDEX'
_JSON_IS_CORRUPT = 'CORRUPT'

_OMITTED = '<omitted>'


def main(args):
   records = _readDB(args.dbCsv, args.csvDelimiter)
   print('DB extract contains {} EAM records'.format(len(records)))

   eamState = {
      _JSON_COUNTERS: _extractCounters(records),
      _JSON_AGENCIES: _extractAgencies(records, args.omitEncoded)
   }
   print(
      '{} named counter(s) referenced.'.format(len(eamState[_JSON_COUNTERS]))
   )
   print('{} agency(ies) referenced.'.format(len(eamState[_JSON_AGENCIES])))
   print(
      '{} agent(s) referenced.'.format(
         sum(
            len(eamState[_JSON_AGENCIES][agency][_JSON_AGENTS])
            for agency in eamState[_JSON_AGENCIES]
         )
      )
   )

   _dumpState(args.jsonOut, eamState)

   _scanForIndexInconsistencies(eamState[_JSON_AGENCIES])


def _scanForIndexInconsistencies(agencies):
   agencyIndices = tuple(
      agencies[agency][_JSON_DB_INDEX] for agency in agencies
   )
   if len(agencyIndices) > 0:
      missingIndices = filter(
         lambda x: x not in agencyIndices,
         xrange(max(agencyIndices))
      )
      if len(missingIndices) != 0:
         print('Missing Agency mapping indices: {}'.format(missingIndices))
      for agency in agencies:
         _scanForMissingAgentIndices(agency, agencies[agency])


def _scanForMissingAgentIndices(agencyId, agencyData):
   agentIndices = tuple(
      agencyData[_JSON_AGENTS][agent][_JSON_DB_INDEX]
      for agent in agencyData[_JSON_AGENTS]
   )
   if len(agentIndices) > 0:
      missingIndices = filter(
         lambda x: x not in agentIndices,
         xrange(max(agentIndices))
      )
      if len(missingIndices) != 0:
         print(
            'Agency {} is missing agent mapping indices: {}'.format(
               agencyId,
               missingIndices
            )
         )


def _dumpState(outFileName, savedState):
   print('Dumping parsed DB data to {}'.format(outFileName))
   with codecOpen(outFileName, 'w', encoding='utf-8') as fout:
      dump(savedState, fout, indent=3)
   print('DB successfully written to {}.'.format(outFileName))


def _extractAgencies(records, omitEncoded):
   def __agencyKeyMatch(dbKey):
      return (
         dbKey is not None and
         _AGENCY_IDX_PREFIX in dbKey and
         dbKey.endswith(_AGENCY_IDX_SUFFIX)
      )

   agencyMapKeys = _findKeys(
      records,
      __agencyKeyMatch
   )
   agencies = (
      (_extractValue(records, agencyKey), agencyKey)
      for agencyKey in agencyMapKeys
   )
   return {
      agency[0]: _extractAgency(records, agency[0], agency[1], omitEncoded)
      for agency in agencies
   }


def _extractAgency(records, agencyId, agencyMapKey, omitEncoded):
   dbIndex = agencyMapKey[
      agencyMapKey.find(_AGENCY_IDX_PREFIX) + len(_AGENCY_IDX_PREFIX):
      -len(_AGENCY_IDX_SUFFIX)
   ]
   isExtension = _extractValue(records, _AGENCY_IS_EXT.format(agencyId))
   goalState = _extractValue(records, _AGENCY_GOAL_STATE.format(agencyId))
   extKey = _extractValue(records, _AGENCY_EXT_KEY.format(agencyId))
   config = _extractValue(records, _AGENCY_CONFIG.format(agencyId))
   solName = _extractValue(records, _AGENCY_SOL_NAME.format(agencyId))

   return {
      _JSON_DB_INDEX: int(dbIndex),
      _JSON_AGENCY_IS_EXT: isExtension,
      _JSON_AGENCY_GOAL_STATE: goalState,
      _JSON_AGENCY_EXT_KEY: extKey,
      _JSON_AGENCY_CONFIG: _OMITTED if omitEncoded else config,
      _JSON_AGENCY_SOL_NAME: solName,
      _JSON_IS_CORRUPT: None in (
         isExtension, goalState, extKey, config, solName
      ),
      _JSON_AGENTS: _extractAgents(records, agencyId, omitEncoded),
   }


def _extractAgents(records, agencyId, omitEncoded):
   def __createAgentKeyMatch(prefix):
      return lambda dbKey: (
         dbKey is not None and
         dbKey.startswith(prefix) and
         dbKey.endswith(_AGENT_IDX_SUFFIX)
      )

   agentMapPrefix = _AGENT_IDX_PREFIX.format(agencyId)
   agentMapKeys = _findKeys(
      records,
      __createAgentKeyMatch(agentMapPrefix)
   )
   agents = (
      (_extractValue(records, agentKey), agentKey)
      for agentKey in agentMapKeys
   )
   return {
      agent[0]: _extractAgent(
         records,
         agentMapPrefix,
         agent[0],
         agent[1],
         omitEncoded
      )
      for agent in agents
   }


def _extractAgent(records, agentMapPrefix, agentId, agentMapKey, omitEncoded):
   dbIndex = agentMapKey[len(agentMapPrefix):-len(_AGENT_IDX_SUFFIX)]
   goalState = _extractValue(records, _AGENT_GOAL_STATE.format(agentId))
   nicToIp = _extractValue(records, _AGENT_NIC_TO_IP.format(agentId))
   host = _extractValue(records, _AGENT_HOST.format(agentId))
   wasUpgrading = _extractValue(records, _AGENT_WAS_UPGRADING.format(agentId))
   isUpgrading = _extractValue(records, _AGENT_IS_UPGRADING.format(agentId))
   baseOvfEnv = _extractValue(records, _AGENT_BASE_OVF_ENV.format(agentId))
   rebootAfter = _extractValue(records, _AGENT_REBOOT_AFTER.format(agentId))
   config = _extractValue(records, _AGENT_CONFIG.format(agentId))

   return {
      _JSON_DB_INDEX: int(dbIndex),
      _JSON_AGENT_GOAL_STATE: goalState,
      _JSON_AGENT_NIC_TO_IP: _OMITTED if omitEncoded else nicToIp,
      _JSON_AGENT_HOST: host,
      _JSON_AGENT_WAS_UPGRADING: wasUpgrading,
      _JSON_AGENT_IS_UPGRADING: isUpgrading,
      _JSON_AGENT_BASE_OVF_ENV: _OMITTED if omitEncoded else baseOvfEnv,
      _JSON_AGENT_REBOOT_AFTER: rebootAfter,
      _JSON_AGENT_CONFIG: _OMITTED if omitEncoded else config,
      _JSON_IS_CORRUPT: None in (
         goalState,
         nicToIp,
         host,
         wasUpgrading,
         isUpgrading,
         baseOvfEnv,
         rebootAfter,
         config
      )
   }


def _extractCounters(records):
   counters = frozenset(
      _findKeys(
         records,
         _prefixMatcher(_GLOBAL_NAME_REF),
         _prefixRemover(_GLOBAL_NAME_REF)
      ) +
      _findKeys(
         records,
         _prefixMatcher(_GLOBAL_NAME_CNT),
         _prefixRemover(_GLOBAL_NAME_CNT)
      )
   )

   return {
      counter: _extractCounter(records, counter)
      for counter in counters
   }


def _extractCounter(records, counterName):
   refs = _extractValue(records, _GLOBAL_NAME_REF + counterName)
   count = _extractValue(records, _GLOBAL_NAME_CNT + counterName)
   return {
      _JSON_COUNTER_REFS: refs,
      _JSON_COUNTER_VALUE: count,
      _JSON_IS_CORRUPT: None in (refs, count)
   }


def _prefixMatcher(prefix):
   return lambda x: x is not None and x.startswith(prefix)


def _prefixRemover(prefix):
   return lambda x: None if x is None else x[len(prefix):]


def _findKeys(records, matcher, formatter=lambda x: x):
   return tuple(
      formatter(rec.get(_KEY)) for rec in records if matcher(rec.get(_KEY))
   )


def _extractValue(records, recKey):
   return next(
      (rec.get(_VALUE) for rec in records if rec.get(_KEY) == recKey),
      None
   )


def _readDB(dbCsv, csvDelimiter=None):
   try:
      return _parseCsv(dbCsv, 'utf-8', csvDelimiter)
   except:
      return _parseCsv(dbCsv, 'utf-8-sig', csvDelimiter)


def _parseCsv(dbCsv, encoding, csvDelimiter=None):
   with codecOpen(dbCsv, 'r', encoding=encoding) as fin:
      rawData = fin.read()

   with closing(StringIO(rawData)) as csvFile:
      hasHeaders = any(_EXT_KEY in rec for rec in DictReader(csvFile))

   with closing(StringIO(rawData)) as csvFile:
      readerArgs = {'strict': True}
      if not hasHeaders:
         readerArgs['fieldnames'] = _CSV_FIELDS
      if csvDelimiter is not None:
         readerArgs['delimiter'] = csvDelimiter

      csvReader = DictReader(csvFile, **readerArgs)
      return tuple(
         rec for rec in csvReader
         if rec.get(_EXT_KEY) == _EAM_EXT_KEY
      )


def _getArgs():
   parser = ArgumentParser(
      prog='parseDB',
      description=(
         'Parses EAM\'s 6.0 DB records into a more humaly readable format'
      )
   )
   parser.add_argument(
      'dbCsv',
      metavar='eam-db-csv',
      help='CSV file containing the extract of EAM\'s DB records.'
   )
   parser.add_argument(
      'jsonOut',
      metavar='json-output-file',
      help='Fully qualified path to a JSON file to contain the parsed DB data.'
   )
   parser.add_argument(
      '--omitEncoded',
      help=(
         'If specified agency\'s congig and agent\'s config, controlNicKeyToIp'
         ' and baseOvfEnvironment properties will not be exported.'
      ),
      action='store_true'
   )
   parser.add_argument(
      '--csvDelimiter',
      metavar='delimiter',
      help=(
         'If specified that character will be used as value delimiter'
         ' for the CSV file.'
      ),
      default=None
   )
   return parser.parse_args()


if __name__ == '__main__':
   main(_getArgs())