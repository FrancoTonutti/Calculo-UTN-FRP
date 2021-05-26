from ifcopenshell.entity_instance import entity_instance


class IfcVirtualGridIntersection(entity_instance):
    pass


class IfcUnitAssignment(entity_instance):
    pass


class IfcTimeSeriesValue(entity_instance):
    pass


class IfcTimeSeries(entity_instance):
    pass


class IfcIrregularTimeSeries(IfcTimeSeries):
    pass


class IfcRegularTimeSeries(IfcTimeSeries):
    pass


class IfcTimePeriod(entity_instance):
    pass


class IfcTableRow(entity_instance):
    pass


class IfcTableColumn(entity_instance):
    pass


class IfcTable(entity_instance):
    pass


class IfcStructuralLoad(entity_instance):
    pass


class IfcStructuralLoadConfiguration(IfcStructuralLoad):
    pass


class IfcStructuralLoadOrResult(IfcStructuralLoad):
    pass


class IfcStructuralLoadStatic(IfcStructuralLoadOrResult):
    pass


class IfcStructuralLoadLinearForce(IfcStructuralLoadStatic):
    pass


class IfcStructuralLoadPlanarForce(IfcStructuralLoadStatic):
    pass


class IfcStructuralLoadSingleDisplacement(IfcStructuralLoadStatic):
    pass


class IfcStructuralLoadSingleDisplacementDistortion(IfcStructuralLoadSingleDisplacement):
    pass


class IfcStructuralLoadSingleForce(IfcStructuralLoadStatic):
    pass


class IfcStructuralLoadSingleForceWarping(IfcStructuralLoadSingleForce):
    pass


class IfcStructuralLoadTemperature(IfcStructuralLoadStatic):
    pass


class IfcSurfaceReinforcementArea(IfcStructuralLoadOrResult):
    pass


class IfcStructuralConnectionCondition(entity_instance):
    pass


class IfcFailureConnectionCondition(IfcStructuralConnectionCondition):
    pass


class IfcSlippageConnectionCondition(IfcStructuralConnectionCondition):
    pass


class IfcShapeAspect(entity_instance):
    pass


class IfcSchedulingTime(entity_instance):
    pass


class IfcEventTime(IfcSchedulingTime):
    pass


class IfcLagTime(IfcSchedulingTime):
    pass


class IfcResourceTime(IfcSchedulingTime):
    pass


class IfcTaskTime(IfcSchedulingTime):
    pass


class IfcTaskTimeRecurring(IfcTaskTime):
    pass


class IfcWorkTime(IfcSchedulingTime):
    pass


class IfcRoot(entity_instance):
    pass


class IfcObjectDefinition(IfcRoot):
    pass


class IfcContext(IfcObjectDefinition):
    pass


class IfcProject(IfcContext):
    pass


class IfcProjectLibrary(IfcContext):
    pass


class IfcObject(IfcObjectDefinition):
    pass


class IfcActor(IfcObject):
    pass


class IfcOccupant(IfcActor):
    pass


class IfcControl(IfcObject):
    pass


class IfcActionRequest(IfcControl):
    pass


class IfcCostItem(IfcControl):
    pass


class IfcCostSchedule(IfcControl):
    pass


class IfcPerformanceHistory(IfcControl):
    pass


class IfcPermit(IfcControl):
    pass


class IfcProjectOrder(IfcControl):
    pass


class IfcWorkCalendar(IfcControl):
    pass


class IfcWorkControl(IfcControl):
    pass


class IfcWorkPlan(IfcWorkControl):
    pass


class IfcWorkSchedule(IfcWorkControl):
    pass


class IfcGroup(IfcObject):
    pass


class IfcAsset(IfcGroup):
    pass


class IfcInventory(IfcGroup):
    pass


class IfcStructuralLoadGroup(IfcGroup):
    pass


class IfcStructuralLoadCase(IfcStructuralLoadGroup):
    pass


class IfcStructuralResultGroup(IfcGroup):
    pass


class IfcSystem(IfcGroup):
    pass


class IfcBuildingSystem(IfcSystem):
    pass


class IfcDistributionSystem(IfcSystem):
    pass


class IfcDistributionCircuit(IfcDistributionSystem):
    pass


class IfcStructuralAnalysisModel(IfcSystem):
    pass


class IfcZone(IfcSystem):
    pass


class IfcProcess(IfcObject):
    pass


class IfcEvent(IfcProcess):
    pass


class IfcProcedure(IfcProcess):
    pass


class IfcTask(IfcProcess):
    pass


class IfcProduct(IfcObject):
    pass


class IfcAnnotation(IfcProduct):
    pass


class IfcElement(IfcProduct):
    pass


class IfcBuildingElement(IfcElement):
    pass


class IfcBeam(IfcBuildingElement):
    pass


class IfcBeamStandardCase(IfcBeam):
    pass


class IfcBuildingElementProxy(IfcBuildingElement):
    pass


class IfcChimney(IfcBuildingElement):
    pass


class IfcColumn(IfcBuildingElement):
    pass


class IfcColumnStandardCase(IfcColumn):
    pass


class IfcCovering(IfcBuildingElement):
    pass


class IfcCurtainWall(IfcBuildingElement):
    pass


class IfcDoor(IfcBuildingElement):
    pass


class IfcDoorStandardCase(IfcDoor):
    pass


class IfcFooting(IfcBuildingElement):
    pass


class IfcMember(IfcBuildingElement):
    pass


class IfcMemberStandardCase(IfcMember):
    pass


class IfcPile(IfcBuildingElement):
    pass


class IfcPlate(IfcBuildingElement):
    pass


class IfcPlateStandardCase(IfcPlate):
    pass


class IfcRailing(IfcBuildingElement):
    pass


class IfcRamp(IfcBuildingElement):
    pass


class IfcRampFlight(IfcBuildingElement):
    pass


class IfcRoof(IfcBuildingElement):
    pass


class IfcShadingDevice(IfcBuildingElement):
    pass


class IfcSlab(IfcBuildingElement):
    pass


class IfcSlabElementedCase(IfcSlab):
    pass


class IfcSlabStandardCase(IfcSlab):
    pass


class IfcStair(IfcBuildingElement):
    pass


class IfcStairFlight(IfcBuildingElement):
    pass


class IfcWall(IfcBuildingElement):
    pass


class IfcWallElementedCase(IfcWall):
    pass


class IfcWallStandardCase(IfcWall):
    pass


class IfcWindow(IfcBuildingElement):
    pass


class IfcWindowStandardCase(IfcWindow):
    pass


class IfcCivilElement(IfcElement):
    pass


class IfcDistributionElement(IfcElement):
    pass


class IfcDistributionControlElement(IfcDistributionElement):
    pass


class IfcActuator(IfcDistributionControlElement):
    pass


class IfcAlarm(IfcDistributionControlElement):
    pass


class IfcController(IfcDistributionControlElement):
    pass


class IfcFlowInstrument(IfcDistributionControlElement):
    pass


class IfcProtectiveDeviceTrippingUnit(IfcDistributionControlElement):
    pass


class IfcSensor(IfcDistributionControlElement):
    pass


class IfcUnitaryControlElement(IfcDistributionControlElement):
    pass


class IfcDistributionFlowElement(IfcDistributionElement):
    pass


class IfcDistributionChamberElement(IfcDistributionFlowElement):
    pass


class IfcEnergyConversionDevice(IfcDistributionFlowElement):
    pass


class IfcAirToAirHeatRecovery(IfcEnergyConversionDevice):
    pass


class IfcBoiler(IfcEnergyConversionDevice):
    pass


class IfcBurner(IfcEnergyConversionDevice):
    pass


class IfcChiller(IfcEnergyConversionDevice):
    pass


class IfcCoil(IfcEnergyConversionDevice):
    pass


class IfcCondenser(IfcEnergyConversionDevice):
    pass


class IfcCooledBeam(IfcEnergyConversionDevice):
    pass


class IfcCoolingTower(IfcEnergyConversionDevice):
    pass


class IfcElectricGenerator(IfcEnergyConversionDevice):
    pass


class IfcElectricMotor(IfcEnergyConversionDevice):
    pass


class IfcEngine(IfcEnergyConversionDevice):
    pass


class IfcEvaporativeCooler(IfcEnergyConversionDevice):
    pass


class IfcEvaporator(IfcEnergyConversionDevice):
    pass


class IfcHeatExchanger(IfcEnergyConversionDevice):
    pass


class IfcHumidifier(IfcEnergyConversionDevice):
    pass


class IfcMotorConnection(IfcEnergyConversionDevice):
    pass


class IfcSolarDevice(IfcEnergyConversionDevice):
    pass


class IfcTransformer(IfcEnergyConversionDevice):
    pass


class IfcTubeBundle(IfcEnergyConversionDevice):
    pass


class IfcUnitaryEquipment(IfcEnergyConversionDevice):
    pass


class IfcFlowController(IfcDistributionFlowElement):
    pass


class IfcAirTerminalBox(IfcFlowController):
    pass


class IfcDamper(IfcFlowController):
    pass


class IfcElectricDistributionBoard(IfcFlowController):
    pass


class IfcElectricTimeControl(IfcFlowController):
    pass


class IfcFlowMeter(IfcFlowController):
    pass


class IfcProtectiveDevice(IfcFlowController):
    pass


class IfcSwitchingDevice(IfcFlowController):
    pass


class IfcValve(IfcFlowController):
    pass


class IfcFlowFitting(IfcDistributionFlowElement):
    pass


class IfcCableCarrierFitting(IfcFlowFitting):
    pass


class IfcCableFitting(IfcFlowFitting):
    pass


class IfcDuctFitting(IfcFlowFitting):
    pass


class IfcJunctionBox(IfcFlowFitting):
    pass


class IfcPipeFitting(IfcFlowFitting):
    pass


class IfcFlowMovingDevice(IfcDistributionFlowElement):
    pass


class IfcCompressor(IfcFlowMovingDevice):
    pass


class IfcFan(IfcFlowMovingDevice):
    pass


class IfcPump(IfcFlowMovingDevice):
    pass


class IfcFlowSegment(IfcDistributionFlowElement):
    pass


class IfcCableCarrierSegment(IfcFlowSegment):
    pass


class IfcCableSegment(IfcFlowSegment):
    pass


class IfcDuctSegment(IfcFlowSegment):
    pass


class IfcPipeSegment(IfcFlowSegment):
    pass


class IfcFlowStorageDevice(IfcDistributionFlowElement):
    pass


class IfcElectricFlowStorageDevice(IfcFlowStorageDevice):
    pass


class IfcTank(IfcFlowStorageDevice):
    pass


class IfcFlowTerminal(IfcDistributionFlowElement):
    pass


class IfcAirTerminal(IfcFlowTerminal):
    pass


class IfcAudioVisualAppliance(IfcFlowTerminal):
    pass


class IfcCommunicationsAppliance(IfcFlowTerminal):
    pass


class IfcElectricAppliance(IfcFlowTerminal):
    pass


class IfcFireSuppressionTerminal(IfcFlowTerminal):
    pass


class IfcLamp(IfcFlowTerminal):
    pass


class IfcLightFixture(IfcFlowTerminal):
    pass


class IfcMedicalDevice(IfcFlowTerminal):
    pass


class IfcOutlet(IfcFlowTerminal):
    pass


class IfcSanitaryTerminal(IfcFlowTerminal):
    pass


class IfcSpaceHeater(IfcFlowTerminal):
    pass


class IfcStackTerminal(IfcFlowTerminal):
    pass


class IfcWasteTerminal(IfcFlowTerminal):
    pass


class IfcFlowTreatmentDevice(IfcDistributionFlowElement):
    pass


class IfcDuctSilencer(IfcFlowTreatmentDevice):
    pass


class IfcFilter(IfcFlowTreatmentDevice):
    pass


class IfcInterceptor(IfcFlowTreatmentDevice):
    pass


class IfcElementAssembly(IfcElement):
    pass


class IfcElementComponent(IfcElement):
    pass


class IfcBuildingElementPart(IfcElementComponent):
    pass


class IfcDiscreteAccessory(IfcElementComponent):
    pass


class IfcFastener(IfcElementComponent):
    pass


class IfcMechanicalFastener(IfcElementComponent):
    pass


class IfcReinforcingElement(IfcElementComponent):
    pass


class IfcReinforcingBar(IfcReinforcingElement):
    pass


class IfcReinforcingMesh(IfcReinforcingElement):
    pass


class IfcTendon(IfcReinforcingElement):
    pass


class IfcTendonAnchor(IfcReinforcingElement):
    pass


class IfcVibrationIsolator(IfcElementComponent):
    pass


class IfcFeatureElement(IfcElement):
    pass


class IfcFeatureElementAddition(IfcFeatureElement):
    pass


class IfcProjectionElement(IfcFeatureElementAddition):
    pass


class IfcFeatureElementSubtraction(IfcFeatureElement):
    pass


class IfcOpeningElement(IfcFeatureElementSubtraction):
    pass


class IfcOpeningStandardCase(IfcOpeningElement):
    pass


class IfcVoidingFeature(IfcFeatureElementSubtraction):
    pass


class IfcSurfaceFeature(IfcFeatureElement):
    pass


class IfcFurnishingElement(IfcElement):
    pass


class IfcFurniture(IfcFurnishingElement):
    pass


class IfcSystemFurnitureElement(IfcFurnishingElement):
    pass


class IfcGeographicElement(IfcElement):
    pass


class IfcTransportElement(IfcElement):
    pass


class IfcVirtualElement(IfcElement):
    pass


class IfcPort(IfcProduct):
    pass


class IfcDistributionPort(IfcPort):
    pass


class IfcPositioningElement(IfcProduct):
    pass


class IfcGrid(IfcPositioningElement):
    pass


class IfcLinearPositioningElement(IfcPositioningElement):
    pass


class IfcAlignment(IfcLinearPositioningElement):
    pass


class IfcReferent(IfcPositioningElement):
    pass


class IfcProxy(IfcProduct):
    pass


class IfcSpatialElement(IfcProduct):
    pass


class IfcExternalSpatialStructureElement(IfcSpatialElement):
    pass


class IfcExternalSpatialElement(IfcExternalSpatialStructureElement):
    pass


class IfcSpatialStructureElement(IfcSpatialElement):
    pass


class IfcBuilding(IfcSpatialStructureElement):
    pass


class IfcBuildingStorey(IfcSpatialStructureElement):
    pass


class IfcSite(IfcSpatialStructureElement):
    pass


class IfcSpace(IfcSpatialStructureElement):
    pass


class IfcSpatialZone(IfcSpatialElement):
    pass


class IfcStructuralActivity(IfcProduct):
    pass


class IfcStructuralAction(IfcStructuralActivity):
    pass


class IfcStructuralCurveAction(IfcStructuralAction):
    pass


class IfcStructuralLinearAction(IfcStructuralCurveAction):
    pass


class IfcStructuralPointAction(IfcStructuralAction):
    pass


class IfcStructuralSurfaceAction(IfcStructuralAction):
    pass


class IfcStructuralPlanarAction(IfcStructuralSurfaceAction):
    pass


class IfcStructuralReaction(IfcStructuralActivity):
    pass


class IfcStructuralCurveReaction(IfcStructuralReaction):
    pass


class IfcStructuralPointReaction(IfcStructuralReaction):
    pass


class IfcStructuralSurfaceReaction(IfcStructuralReaction):
    pass


class IfcStructuralItem(IfcProduct):
    pass


class IfcStructuralConnection(IfcStructuralItem):
    pass


class IfcStructuralCurveConnection(IfcStructuralConnection):
    pass


class IfcStructuralPointConnection(IfcStructuralConnection):
    pass


class IfcStructuralSurfaceConnection(IfcStructuralConnection):
    pass


class IfcStructuralMember(IfcStructuralItem):
    pass


class IfcStructuralCurveMember(IfcStructuralMember):
    pass


class IfcStructuralCurveMemberVarying(IfcStructuralCurveMember):
    pass


class IfcStructuralSurfaceMember(IfcStructuralMember):
    pass


class IfcStructuralSurfaceMemberVarying(IfcStructuralSurfaceMember):
    pass


class IfcResource(IfcObject):
    pass


class IfcConstructionResource(IfcResource):
    pass


class IfcConstructionEquipmentResource(IfcConstructionResource):
    pass


class IfcConstructionMaterialResource(IfcConstructionResource):
    pass


class IfcConstructionProductResource(IfcConstructionResource):
    pass


class IfcCrewResource(IfcConstructionResource):
    pass


class IfcLaborResource(IfcConstructionResource):
    pass


class IfcSubContractResource(IfcConstructionResource):
    pass


class IfcTypeObject(IfcObjectDefinition):
    pass


class IfcTypeProcess(IfcTypeObject):
    pass


class IfcEventType(IfcTypeProcess):
    pass


class IfcProcedureType(IfcTypeProcess):
    pass


class IfcTaskType(IfcTypeProcess):
    pass


class IfcTypeProduct(IfcTypeObject):
    pass


class IfcDoorStyle(IfcTypeProduct):
    pass


class IfcElementType(IfcTypeProduct):
    pass


class IfcBuildingElementType(IfcElementType):
    pass


class IfcBeamType(IfcBuildingElementType):
    pass


class IfcBuildingElementProxyType(IfcBuildingElementType):
    pass


class IfcChimneyType(IfcBuildingElementType):
    pass


class IfcColumnType(IfcBuildingElementType):
    pass


class IfcCoveringType(IfcBuildingElementType):
    pass


class IfcCurtainWallType(IfcBuildingElementType):
    pass


class IfcDoorType(IfcBuildingElementType):
    pass


class IfcFootingType(IfcBuildingElementType):
    pass


class IfcMemberType(IfcBuildingElementType):
    pass


class IfcPileType(IfcBuildingElementType):
    pass


class IfcPlateType(IfcBuildingElementType):
    pass


class IfcRailingType(IfcBuildingElementType):
    pass


class IfcRampFlightType(IfcBuildingElementType):
    pass


class IfcRampType(IfcBuildingElementType):
    pass


class IfcRoofType(IfcBuildingElementType):
    pass


class IfcShadingDeviceType(IfcBuildingElementType):
    pass


class IfcSlabType(IfcBuildingElementType):
    pass


class IfcStairFlightType(IfcBuildingElementType):
    pass


class IfcStairType(IfcBuildingElementType):
    pass


class IfcWallType(IfcBuildingElementType):
    pass


class IfcWindowType(IfcBuildingElementType):
    pass


class IfcCivilElementType(IfcElementType):
    pass


class IfcDistributionElementType(IfcElementType):
    pass


class IfcDistributionControlElementType(IfcDistributionElementType):
    pass


class IfcActuatorType(IfcDistributionControlElementType):
    pass


class IfcAlarmType(IfcDistributionControlElementType):
    pass


class IfcControllerType(IfcDistributionControlElementType):
    pass


class IfcFlowInstrumentType(IfcDistributionControlElementType):
    pass


class IfcProtectiveDeviceTrippingUnitType(IfcDistributionControlElementType):
    pass


class IfcSensorType(IfcDistributionControlElementType):
    pass


class IfcUnitaryControlElementType(IfcDistributionControlElementType):
    pass


class IfcDistributionFlowElementType(IfcDistributionElementType):
    pass


class IfcDistributionChamberElementType(IfcDistributionFlowElementType):
    pass


class IfcEnergyConversionDeviceType(IfcDistributionFlowElementType):
    pass


class IfcAirToAirHeatRecoveryType(IfcEnergyConversionDeviceType):
    pass


class IfcBoilerType(IfcEnergyConversionDeviceType):
    pass


class IfcBurnerType(IfcEnergyConversionDeviceType):
    pass


class IfcChillerType(IfcEnergyConversionDeviceType):
    pass


class IfcCoilType(IfcEnergyConversionDeviceType):
    pass


class IfcCondenserType(IfcEnergyConversionDeviceType):
    pass


class IfcCooledBeamType(IfcEnergyConversionDeviceType):
    pass


class IfcCoolingTowerType(IfcEnergyConversionDeviceType):
    pass


class IfcElectricGeneratorType(IfcEnergyConversionDeviceType):
    pass


class IfcElectricMotorType(IfcEnergyConversionDeviceType):
    pass


class IfcEngineType(IfcEnergyConversionDeviceType):
    pass


class IfcEvaporativeCoolerType(IfcEnergyConversionDeviceType):
    pass


class IfcEvaporatorType(IfcEnergyConversionDeviceType):
    pass


class IfcHeatExchangerType(IfcEnergyConversionDeviceType):
    pass


class IfcHumidifierType(IfcEnergyConversionDeviceType):
    pass


class IfcMotorConnectionType(IfcEnergyConversionDeviceType):
    pass


class IfcSolarDeviceType(IfcEnergyConversionDeviceType):
    pass


class IfcTransformerType(IfcEnergyConversionDeviceType):
    pass


class IfcTubeBundleType(IfcEnergyConversionDeviceType):
    pass


class IfcUnitaryEquipmentType(IfcEnergyConversionDeviceType):
    pass


class IfcFlowControllerType(IfcDistributionFlowElementType):
    pass


class IfcAirTerminalBoxType(IfcFlowControllerType):
    pass


class IfcDamperType(IfcFlowControllerType):
    pass


class IfcElectricDistributionBoardType(IfcFlowControllerType):
    pass


class IfcElectricTimeControlType(IfcFlowControllerType):
    pass


class IfcFlowMeterType(IfcFlowControllerType):
    pass


class IfcProtectiveDeviceType(IfcFlowControllerType):
    pass


class IfcSwitchingDeviceType(IfcFlowControllerType):
    pass


class IfcValveType(IfcFlowControllerType):
    pass


class IfcFlowFittingType(IfcDistributionFlowElementType):
    pass


class IfcCableCarrierFittingType(IfcFlowFittingType):
    pass


class IfcCableFittingType(IfcFlowFittingType):
    pass


class IfcDuctFittingType(IfcFlowFittingType):
    pass


class IfcJunctionBoxType(IfcFlowFittingType):
    pass


class IfcPipeFittingType(IfcFlowFittingType):
    pass


class IfcFlowMovingDeviceType(IfcDistributionFlowElementType):
    pass


class IfcCompressorType(IfcFlowMovingDeviceType):
    pass


class IfcFanType(IfcFlowMovingDeviceType):
    pass


class IfcPumpType(IfcFlowMovingDeviceType):
    pass


class IfcFlowSegmentType(IfcDistributionFlowElementType):
    pass


class IfcCableCarrierSegmentType(IfcFlowSegmentType):
    pass


class IfcCableSegmentType(IfcFlowSegmentType):
    pass


class IfcDuctSegmentType(IfcFlowSegmentType):
    pass


class IfcPipeSegmentType(IfcFlowSegmentType):
    pass


class IfcFlowStorageDeviceType(IfcDistributionFlowElementType):
    pass


class IfcElectricFlowStorageDeviceType(IfcFlowStorageDeviceType):
    pass


class IfcTankType(IfcFlowStorageDeviceType):
    pass


class IfcFlowTerminalType(IfcDistributionFlowElementType):
    pass


class IfcAirTerminalType(IfcFlowTerminalType):
    pass


class IfcAudioVisualApplianceType(IfcFlowTerminalType):
    pass


class IfcCommunicationsApplianceType(IfcFlowTerminalType):
    pass


class IfcElectricApplianceType(IfcFlowTerminalType):
    pass


class IfcFireSuppressionTerminalType(IfcFlowTerminalType):
    pass


class IfcLampType(IfcFlowTerminalType):
    pass


class IfcLightFixtureType(IfcFlowTerminalType):
    pass


class IfcMedicalDeviceType(IfcFlowTerminalType):
    pass


class IfcOutletType(IfcFlowTerminalType):
    pass


class IfcSanitaryTerminalType(IfcFlowTerminalType):
    pass


class IfcSpaceHeaterType(IfcFlowTerminalType):
    pass


class IfcStackTerminalType(IfcFlowTerminalType):
    pass


class IfcWasteTerminalType(IfcFlowTerminalType):
    pass


class IfcFlowTreatmentDeviceType(IfcDistributionFlowElementType):
    pass


class IfcDuctSilencerType(IfcFlowTreatmentDeviceType):
    pass


class IfcFilterType(IfcFlowTreatmentDeviceType):
    pass


class IfcInterceptorType(IfcFlowTreatmentDeviceType):
    pass


class IfcElementAssemblyType(IfcElementType):
    pass


class IfcElementComponentType(IfcElementType):
    pass


class IfcBuildingElementPartType(IfcElementComponentType):
    pass


class IfcDiscreteAccessoryType(IfcElementComponentType):
    pass


class IfcFastenerType(IfcElementComponentType):
    pass


class IfcMechanicalFastenerType(IfcElementComponentType):
    pass


class IfcReinforcingElementType(IfcElementComponentType):
    pass


class IfcReinforcingBarType(IfcReinforcingElementType):
    pass


class IfcReinforcingMeshType(IfcReinforcingElementType):
    pass


class IfcTendonAnchorType(IfcReinforcingElementType):
    pass


class IfcTendonType(IfcReinforcingElementType):
    pass


class IfcVibrationIsolatorType(IfcElementComponentType):
    pass


class IfcFurnishingElementType(IfcElementType):
    pass


class IfcFurnitureType(IfcFurnishingElementType):
    pass


class IfcSystemFurnitureElementType(IfcFurnishingElementType):
    pass


class IfcGeographicElementType(IfcElementType):
    pass


class IfcTransportElementType(IfcElementType):
    pass


class IfcSpatialElementType(IfcTypeProduct):
    pass


class IfcSpatialStructureElementType(IfcSpatialElementType):
    pass


class IfcSpaceType(IfcSpatialStructureElementType):
    pass


class IfcSpatialZoneType(IfcSpatialElementType):
    pass


class IfcWindowStyle(IfcTypeProduct):
    pass


class IfcTypeResource(IfcTypeObject):
    pass


class IfcConstructionResourceType(IfcTypeResource):
    pass


class IfcConstructionEquipmentResourceType(IfcConstructionResourceType):
    pass


class IfcConstructionMaterialResourceType(IfcConstructionResourceType):
    pass


class IfcConstructionProductResourceType(IfcConstructionResourceType):
    pass


class IfcCrewResourceType(IfcConstructionResourceType):
    pass


class IfcLaborResourceType(IfcConstructionResourceType):
    pass


class IfcSubContractResourceType(IfcConstructionResourceType):
    pass


class IfcPropertyDefinition(IfcRoot):
    pass


class IfcPropertySetDefinition(IfcPropertyDefinition):
    pass


class IfcPreDefinedPropertySet(IfcPropertySetDefinition):
    pass


class IfcDoorLiningProperties(IfcPreDefinedPropertySet):
    pass


class IfcDoorPanelProperties(IfcPreDefinedPropertySet):
    pass


class IfcPermeableCoveringProperties(IfcPreDefinedPropertySet):
    pass


class IfcReinforcementDefinitionProperties(IfcPreDefinedPropertySet):
    pass


class IfcWindowLiningProperties(IfcPreDefinedPropertySet):
    pass


class IfcWindowPanelProperties(IfcPreDefinedPropertySet):
    pass


class IfcPropertySet(IfcPropertySetDefinition):
    pass


class IfcQuantitySet(IfcPropertySetDefinition):
    pass


class IfcElementQuantity(IfcQuantitySet):
    pass


class IfcPropertyTemplateDefinition(IfcPropertyDefinition):
    pass


class IfcPropertySetTemplate(IfcPropertyTemplateDefinition):
    pass


class IfcPropertyTemplate(IfcPropertyTemplateDefinition):
    pass


class IfcComplexPropertyTemplate(IfcPropertyTemplate):
    pass


class IfcSimplePropertyTemplate(IfcPropertyTemplate):
    pass


class IfcRelationship(IfcRoot):
    pass


class IfcRelAssigns(IfcRelationship):
    pass


class IfcRelAssignsToActor(IfcRelAssigns):
    pass


class IfcRelAssignsToControl(IfcRelAssigns):
    pass


class IfcRelAssignsToGroup(IfcRelAssigns):
    pass


class IfcRelAssignsToGroupByFactor(IfcRelAssignsToGroup):
    pass


class IfcRelAssignsToProcess(IfcRelAssigns):
    pass


class IfcRelAssignsToProduct(IfcRelAssigns):
    pass


class IfcRelAssignsToResource(IfcRelAssigns):
    pass


class IfcRelAssociates(IfcRelationship):
    pass


class IfcRelAssociatesApproval(IfcRelAssociates):
    pass


class IfcRelAssociatesClassification(IfcRelAssociates):
    pass


class IfcRelAssociatesConstraint(IfcRelAssociates):
    pass


class IfcRelAssociatesDocument(IfcRelAssociates):
    pass


class IfcRelAssociatesLibrary(IfcRelAssociates):
    pass


class IfcRelAssociatesMaterial(IfcRelAssociates):
    pass


class IfcRelConnects(IfcRelationship):
    pass


class IfcRelConnectsElements(IfcRelConnects):
    pass


class IfcRelConnectsPathElements(IfcRelConnectsElements):
    pass


class IfcRelConnectsWithRealizingElements(IfcRelConnectsElements):
    pass


class IfcRelConnectsPortToElement(IfcRelConnects):
    pass


class IfcRelConnectsPorts(IfcRelConnects):
    pass


class IfcRelConnectsStructuralActivity(IfcRelConnects):
    pass


class IfcRelConnectsStructuralMember(IfcRelConnects):
    pass


class IfcRelConnectsWithEccentricity(IfcRelConnectsStructuralMember):
    pass


class IfcRelContainedInSpatialStructure(IfcRelConnects):
    pass


class IfcRelCoversBldgElements(IfcRelConnects):
    pass


class IfcRelCoversSpaces(IfcRelConnects):
    pass


class IfcRelFillsElement(IfcRelConnects):
    pass


class IfcRelFlowControlElements(IfcRelConnects):
    pass


class IfcRelInterferesElements(IfcRelConnects):
    pass


class IfcRelReferencedInSpatialStructure(IfcRelConnects):
    pass


class IfcRelSequence(IfcRelConnects):
    pass


class IfcRelServicesBuildings(IfcRelConnects):
    pass


class IfcRelSpaceBoundary(IfcRelConnects):
    pass


class IfcRelSpaceBoundary1stLevel(IfcRelSpaceBoundary):
    pass


class IfcRelSpaceBoundary2ndLevel(IfcRelSpaceBoundary1stLevel):
    pass


class IfcRelDeclares(IfcRelationship):
    pass


class IfcRelDecomposes(IfcRelationship):
    pass


class IfcRelAggregates(IfcRelDecomposes):
    pass


class IfcRelNests(IfcRelDecomposes):
    pass


class IfcRelProjectsElement(IfcRelDecomposes):
    pass


class IfcRelVoidsElement(IfcRelDecomposes):
    pass


class IfcRelDefines(IfcRelationship):
    pass


class IfcRelDefinesByObject(IfcRelDefines):
    pass


class IfcRelDefinesByProperties(IfcRelDefines):
    pass


class IfcRelDefinesByTemplate(IfcRelDefines):
    pass


class IfcRelDefinesByType(IfcRelDefines):
    pass


class IfcResourceLevelRelationship(entity_instance):
    pass


class IfcApprovalRelationship(IfcResourceLevelRelationship):
    pass


class IfcCurrencyRelationship(IfcResourceLevelRelationship):
    pass


class IfcDocumentInformationRelationship(IfcResourceLevelRelationship):
    pass


class IfcExternalReferenceRelationship(IfcResourceLevelRelationship):
    pass


class IfcMaterialRelationship(IfcResourceLevelRelationship):
    pass


class IfcOrganizationRelationship(IfcResourceLevelRelationship):
    pass


class IfcPropertyDependencyRelationship(IfcResourceLevelRelationship):
    pass


class IfcResourceApprovalRelationship(IfcResourceLevelRelationship):
    pass


class IfcResourceConstraintRelationship(IfcResourceLevelRelationship):
    pass


class IfcRepresentationMap(entity_instance):
    pass


class IfcRepresentationItem(entity_instance):
    pass


class IfcGeometricRepresentationItem(IfcRepresentationItem):
    pass


class IfcAlignment2DHorizontal(IfcGeometricRepresentationItem):
    pass


class IfcAlignment2DSegment(IfcGeometricRepresentationItem):
    pass


class IfcAlignment2DHorizontalSegment(IfcAlignment2DSegment):
    pass


class IfcAlignment2DVerticalSegment(IfcAlignment2DSegment):
    pass


class IfcAlignment2DVerSegCircularArc(IfcAlignment2DVerticalSegment):
    pass


class IfcAlignment2DVerSegLine(IfcAlignment2DVerticalSegment):
    pass


class IfcAlignment2DVerSegParabolicArc(IfcAlignment2DVerticalSegment):
    pass


class IfcAlignment2DVertical(IfcGeometricRepresentationItem):
    pass


class IfcAnnotationFillArea(IfcGeometricRepresentationItem):
    pass


class IfcBooleanResult(IfcGeometricRepresentationItem):
    pass


class IfcBooleanClippingResult(IfcBooleanResult):
    pass


class IfcBoundingBox(IfcGeometricRepresentationItem):
    pass


class IfcCartesianPointList(IfcGeometricRepresentationItem):
    pass


class IfcCartesianPointList2D(IfcCartesianPointList):
    pass


class IfcCartesianPointList3D(IfcCartesianPointList):
    pass


class IfcCartesianTransformationOperator(IfcGeometricRepresentationItem):
    pass


class IfcCartesianTransformationOperator2D(IfcCartesianTransformationOperator):
    pass


class IfcCartesianTransformationOperator2DnonUniform(IfcCartesianTransformationOperator2D):
    pass


class IfcCartesianTransformationOperator3D(IfcCartesianTransformationOperator):
    pass


class IfcCartesianTransformationOperator3DnonUniform(IfcCartesianTransformationOperator3D):
    pass


class IfcCompositeCurveSegment(IfcGeometricRepresentationItem):
    pass


class IfcReparametrisedCompositeCurveSegment(IfcCompositeCurveSegment):
    pass


class IfcCsgPrimitive3D(IfcGeometricRepresentationItem):
    pass


class IfcBlock(IfcCsgPrimitive3D):
    pass


class IfcRectangularPyramid(IfcCsgPrimitive3D):
    pass


class IfcRightCircularCone(IfcCsgPrimitive3D):
    pass


class IfcRightCircularCylinder(IfcCsgPrimitive3D):
    pass


class IfcSphere(IfcCsgPrimitive3D):
    pass


class IfcCurve(IfcGeometricRepresentationItem):
    pass


class IfcBoundedCurve(IfcCurve):
    pass


class IfcAlignmentCurve(IfcBoundedCurve):
    pass


class IfcBSplineCurve(IfcBoundedCurve):
    pass


class IfcBSplineCurveWithKnots(IfcBSplineCurve):
    pass


class IfcRationalBSplineCurveWithKnots(IfcBSplineCurveWithKnots):
    pass


class IfcCompositeCurve(IfcBoundedCurve):
    pass


class IfcCompositeCurveOnSurface(IfcCompositeCurve):
    pass


class IfcBoundaryCurve(IfcCompositeCurveOnSurface):
    pass


class IfcOuterBoundaryCurve(IfcBoundaryCurve):
    pass


class IfcCurveSegment2D(IfcBoundedCurve):
    pass


class IfcCircularArcSegment2D(IfcCurveSegment2D):
    pass


class IfcLineSegment2D(IfcCurveSegment2D):
    pass


class IfcTransitionCurveSegment2D(IfcCurveSegment2D):
    pass


class IfcIndexedPolyCurve(IfcBoundedCurve):
    pass


class IfcPolyline(IfcBoundedCurve):
    pass


class IfcTrimmedCurve(IfcBoundedCurve):
    pass


class IfcConic(IfcCurve):
    pass


class IfcCircle(IfcConic):
    pass


class IfcEllipse(IfcConic):
    pass


class IfcLine(IfcCurve):
    pass


class IfcOffsetCurve(IfcCurve):
    pass


class IfcOffsetCurve2D(IfcOffsetCurve):
    pass


class IfcOffsetCurve3D(IfcOffsetCurve):
    pass


class IfcOffsetCurveByDistances(IfcOffsetCurve):
    pass


class IfcPcurve(IfcCurve):
    pass


class IfcSurfaceCurve(IfcCurve):
    pass


class IfcIntersectionCurve(IfcSurfaceCurve):
    pass


class IfcSeamCurve(IfcSurfaceCurve):
    pass


class IfcDirection(IfcGeometricRepresentationItem):
    pass


class IfcDistanceExpression(IfcGeometricRepresentationItem):
    pass


class IfcFaceBasedSurfaceModel(IfcGeometricRepresentationItem):
    pass


class IfcFillAreaStyleHatching(IfcGeometricRepresentationItem):
    pass


class IfcFillAreaStyleTiles(IfcGeometricRepresentationItem):
    pass


class IfcGeometricSet(IfcGeometricRepresentationItem):
    pass


class IfcGeometricCurveSet(IfcGeometricSet):
    pass


class IfcHalfSpaceSolid(IfcGeometricRepresentationItem):
    pass


class IfcBoxedHalfSpace(IfcHalfSpaceSolid):
    pass


class IfcPolygonalBoundedHalfSpace(IfcHalfSpaceSolid):
    pass


class IfcLightSource(IfcGeometricRepresentationItem):
    pass


class IfcLightSourceAmbient(IfcLightSource):
    pass


class IfcLightSourceDirectional(IfcLightSource):
    pass


class IfcLightSourceGoniometric(IfcLightSource):
    pass


class IfcLightSourcePositional(IfcLightSource):
    pass


class IfcLightSourceSpot(IfcLightSourcePositional):
    pass


class IfcOrientationExpression(IfcGeometricRepresentationItem):
    pass


class IfcPlacement(IfcGeometricRepresentationItem):
    pass


class IfcAxis1Placement(IfcPlacement):
    pass


class IfcAxis2Placement2D(IfcPlacement):
    pass


class IfcAxis2Placement3D(IfcPlacement):
    pass


class IfcPlanarExtent(IfcGeometricRepresentationItem):
    pass


class IfcPlanarBox(IfcPlanarExtent):
    pass


class IfcPoint(IfcGeometricRepresentationItem):
    pass


class IfcCartesianPoint(IfcPoint):
    pass


class IfcPointOnCurve(IfcPoint):
    pass


class IfcPointOnSurface(IfcPoint):
    pass


class IfcSectionedSpine(IfcGeometricRepresentationItem):
    pass


class IfcShellBasedSurfaceModel(IfcGeometricRepresentationItem):
    pass


class IfcSolidModel(IfcGeometricRepresentationItem):
    pass


class IfcCsgSolid(IfcSolidModel):
    pass


class IfcManifoldSolidBrep(IfcSolidModel):
    pass


class IfcAdvancedBrep(IfcManifoldSolidBrep):
    pass


class IfcAdvancedBrepWithVoids(IfcAdvancedBrep):
    pass


class IfcFacetedBrep(IfcManifoldSolidBrep):
    pass


class IfcFacetedBrepWithVoids(IfcFacetedBrep):
    pass


class IfcSectionedSolid(IfcSolidModel):
    pass


class IfcSectionedSolidHorizontal(IfcSectionedSolid):
    pass


class IfcSweptAreaSolid(IfcSolidModel):
    pass


class IfcExtrudedAreaSolid(IfcSweptAreaSolid):
    pass


class IfcExtrudedAreaSolidTapered(IfcExtrudedAreaSolid):
    pass


class IfcFixedReferenceSweptAreaSolid(IfcSweptAreaSolid):
    pass


class IfcRevolvedAreaSolid(IfcSweptAreaSolid):
    pass


class IfcRevolvedAreaSolidTapered(IfcRevolvedAreaSolid):
    pass


class IfcSurfaceCurveSweptAreaSolid(IfcSweptAreaSolid):
    pass


class IfcSweptDiskSolid(IfcSolidModel):
    pass


class IfcSweptDiskSolidPolygonal(IfcSweptDiskSolid):
    pass


class IfcSurface(IfcGeometricRepresentationItem):
    pass


class IfcBoundedSurface(IfcSurface):
    pass


class IfcBSplineSurface(IfcBoundedSurface):
    pass


class IfcBSplineSurfaceWithKnots(IfcBSplineSurface):
    pass


class IfcRationalBSplineSurfaceWithKnots(IfcBSplineSurfaceWithKnots):
    pass


class IfcCurveBoundedPlane(IfcBoundedSurface):
    pass


class IfcCurveBoundedSurface(IfcBoundedSurface):
    pass


class IfcRectangularTrimmedSurface(IfcBoundedSurface):
    pass


class IfcElementarySurface(IfcSurface):
    pass


class IfcCylindricalSurface(IfcElementarySurface):
    pass


class IfcPlane(IfcElementarySurface):
    pass


class IfcSphericalSurface(IfcElementarySurface):
    pass


class IfcToroidalSurface(IfcElementarySurface):
    pass


class IfcSweptSurface(IfcSurface):
    pass


class IfcSurfaceOfLinearExtrusion(IfcSweptSurface):
    pass


class IfcSurfaceOfRevolution(IfcSweptSurface):
    pass


class IfcTessellatedItem(IfcGeometricRepresentationItem):
    pass


class IfcIndexedPolygonalFace(IfcTessellatedItem):
    pass


class IfcIndexedPolygonalFaceWithVoids(IfcIndexedPolygonalFace):
    pass


class IfcTessellatedFaceSet(IfcTessellatedItem):
    pass


class IfcPolygonalFaceSet(IfcTessellatedFaceSet):
    pass


class IfcTriangulatedFaceSet(IfcTessellatedFaceSet):
    pass


class IfcTriangulatedIrregularNetwork(IfcTriangulatedFaceSet):
    pass


class IfcTextLiteral(IfcGeometricRepresentationItem):
    pass


class IfcTextLiteralWithExtent(IfcTextLiteral):
    pass


class IfcVector(IfcGeometricRepresentationItem):
    pass


class IfcMappedItem(IfcRepresentationItem):
    pass


class IfcStyledItem(IfcRepresentationItem):
    pass


class IfcTopologicalRepresentationItem(IfcRepresentationItem):
    pass


class IfcConnectedFaceSet(IfcTopologicalRepresentationItem):
    pass


class IfcClosedShell(IfcConnectedFaceSet):
    pass


class IfcOpenShell(IfcConnectedFaceSet):
    pass


class IfcEdge(IfcTopologicalRepresentationItem):
    pass


class IfcEdgeCurve(IfcEdge):
    pass


class IfcOrientedEdge(IfcEdge):
    pass


class IfcSubedge(IfcEdge):
    pass


class IfcFace(IfcTopologicalRepresentationItem):
    pass


class IfcFaceSurface(IfcFace):
    pass


class IfcAdvancedFace(IfcFaceSurface):
    pass


class IfcFaceBound(IfcTopologicalRepresentationItem):
    pass


class IfcFaceOuterBound(IfcFaceBound):
    pass


class IfcLoop(IfcTopologicalRepresentationItem):
    pass


class IfcEdgeLoop(IfcLoop):
    pass


class IfcPolyLoop(IfcLoop):
    pass


class IfcVertexLoop(IfcLoop):
    pass


class IfcPath(IfcTopologicalRepresentationItem):
    pass


class IfcVertex(IfcTopologicalRepresentationItem):
    pass


class IfcVertexPoint(IfcVertex):
    pass


class IfcRepresentationContext(entity_instance):
    pass


class IfcGeometricRepresentationContext(IfcRepresentationContext):
    pass


class IfcGeometricRepresentationSubContext(IfcGeometricRepresentationContext):
    pass


class IfcRepresentation(entity_instance):
    pass


class IfcShapeModel(IfcRepresentation):
    pass


class IfcShapeRepresentation(IfcShapeModel):
    pass


class IfcTopologyRepresentation(IfcShapeModel):
    pass


class IfcStyleModel(IfcRepresentation):
    pass


class IfcStyledRepresentation(IfcStyleModel):
    pass


class IfcReference(entity_instance):
    pass


class IfcRecurrencePattern(entity_instance):
    pass


class IfcPropertyAbstraction(entity_instance):
    pass


class IfcExtendedProperties(IfcPropertyAbstraction):
    pass


class IfcMaterialProperties(IfcExtendedProperties):
    pass


class IfcProfileProperties(IfcExtendedProperties):
    pass


class IfcPreDefinedProperties(IfcPropertyAbstraction):
    pass


class IfcReinforcementBarProperties(IfcPreDefinedProperties):
    pass


class IfcSectionProperties(IfcPreDefinedProperties):
    pass


class IfcSectionReinforcementProperties(IfcPreDefinedProperties):
    pass


class IfcProperty(IfcPropertyAbstraction):
    pass


class IfcComplexProperty(IfcProperty):
    pass


class IfcSimpleProperty(IfcProperty):
    pass


class IfcPropertyBoundedValue(IfcSimpleProperty):
    pass


class IfcPropertyEnumeratedValue(IfcSimpleProperty):
    pass


class IfcPropertyListValue(IfcSimpleProperty):
    pass


class IfcPropertyReferenceValue(IfcSimpleProperty):
    pass


class IfcPropertySingleValue(IfcSimpleProperty):
    pass


class IfcPropertyTableValue(IfcSimpleProperty):
    pass


class IfcPropertyEnumeration(IfcPropertyAbstraction):
    pass


class IfcProfileDef(entity_instance):
    pass


class IfcArbitraryClosedProfileDef(IfcProfileDef):
    pass


class IfcArbitraryProfileDefWithVoids(IfcArbitraryClosedProfileDef):
    pass


class IfcArbitraryOpenProfileDef(IfcProfileDef):
    pass


class IfcCenterLineProfileDef(IfcArbitraryOpenProfileDef):
    pass


class IfcCompositeProfileDef(IfcProfileDef):
    pass


class IfcDerivedProfileDef(IfcProfileDef):
    pass


class IfcMirroredProfileDef(IfcDerivedProfileDef):
    pass


class IfcParameterizedProfileDef(IfcProfileDef):
    pass


class IfcAsymmetricIShapeProfileDef(IfcParameterizedProfileDef):
    pass


class IfcCShapeProfileDef(IfcParameterizedProfileDef):
    pass


class IfcCircleProfileDef(IfcParameterizedProfileDef):
    pass


class IfcCircleHollowProfileDef(IfcCircleProfileDef):
    pass


class IfcEllipseProfileDef(IfcParameterizedProfileDef):
    pass


class IfcIShapeProfileDef(IfcParameterizedProfileDef):
    pass


class IfcLShapeProfileDef(IfcParameterizedProfileDef):
    pass


class IfcRectangleProfileDef(IfcParameterizedProfileDef):
    pass


class IfcRectangleHollowProfileDef(IfcRectangleProfileDef):
    pass


class IfcRoundedRectangleProfileDef(IfcRectangleProfileDef):
    pass


class IfcTShapeProfileDef(IfcParameterizedProfileDef):
    pass


class IfcTrapeziumProfileDef(IfcParameterizedProfileDef):
    pass


class IfcUShapeProfileDef(IfcParameterizedProfileDef):
    pass


class IfcZShapeProfileDef(IfcParameterizedProfileDef):
    pass


class IfcProductRepresentation(entity_instance):
    pass


class IfcMaterialDefinitionRepresentation(IfcProductRepresentation):
    pass


class IfcProductDefinitionShape(IfcProductRepresentation):
    pass


class IfcPresentationStyleAssignment(entity_instance):
    pass


class IfcPresentationStyle(entity_instance):
    pass


class IfcCurveStyle(IfcPresentationStyle):
    pass


class IfcFillAreaStyle(IfcPresentationStyle):
    pass


class IfcSurfaceStyle(IfcPresentationStyle):
    pass


class IfcTextStyle(IfcPresentationStyle):
    pass


class IfcPresentationLayerAssignment(entity_instance):
    pass


class IfcPresentationLayerWithStyle(IfcPresentationLayerAssignment):
    pass


class IfcPresentationItem(entity_instance):
    pass


class IfcColourRgbList(IfcPresentationItem):
    pass


class IfcColourSpecification(IfcPresentationItem):
    pass


class IfcColourRgb(IfcColourSpecification):
    pass


class IfcCurveStyleFont(IfcPresentationItem):
    pass


class IfcCurveStyleFontAndScaling(IfcPresentationItem):
    pass


class IfcCurveStyleFontPattern(IfcPresentationItem):
    pass


class IfcIndexedColourMap(IfcPresentationItem):
    pass


class IfcPreDefinedItem(IfcPresentationItem):
    pass


class IfcPreDefinedColour(IfcPreDefinedItem):
    pass


class IfcDraughtingPreDefinedColour(IfcPreDefinedColour):
    pass


class IfcPreDefinedCurveFont(IfcPreDefinedItem):
    pass


class IfcDraughtingPreDefinedCurveFont(IfcPreDefinedCurveFont):
    pass


class IfcPreDefinedTextFont(IfcPreDefinedItem):
    pass


class IfcTextStyleFontModel(IfcPreDefinedTextFont):
    pass


class IfcSurfaceStyleLighting(IfcPresentationItem):
    pass


class IfcSurfaceStyleRefraction(IfcPresentationItem):
    pass


class IfcSurfaceStyleShading(IfcPresentationItem):
    pass


class IfcSurfaceStyleRendering(IfcSurfaceStyleShading):
    pass


class IfcSurfaceStyleWithTextures(IfcPresentationItem):
    pass


class IfcSurfaceTexture(IfcPresentationItem):
    pass


class IfcBlobTexture(IfcSurfaceTexture):
    pass


class IfcImageTexture(IfcSurfaceTexture):
    pass


class IfcPixelTexture(IfcSurfaceTexture):
    pass


class IfcTextStyleForDefinedFont(IfcPresentationItem):
    pass


class IfcTextStyleTextModel(IfcPresentationItem):
    pass


class IfcTextureCoordinate(IfcPresentationItem):
    pass


class IfcIndexedTextureMap(IfcTextureCoordinate):
    pass


class IfcIndexedTriangleTextureMap(IfcIndexedTextureMap):
    pass


class IfcTextureCoordinateGenerator(IfcTextureCoordinate):
    pass


class IfcTextureMap(IfcTextureCoordinate):
    pass


class IfcTextureVertex(IfcPresentationItem):
    pass


class IfcTextureVertexList(IfcPresentationItem):
    pass


class IfcPhysicalQuantity(entity_instance):
    pass


class IfcPhysicalComplexQuantity(IfcPhysicalQuantity):
    pass


class IfcPhysicalSimpleQuantity(IfcPhysicalQuantity):
    pass


class IfcQuantityArea(IfcPhysicalSimpleQuantity):
    pass


class IfcQuantityCount(IfcPhysicalSimpleQuantity):
    pass


class IfcQuantityLength(IfcPhysicalSimpleQuantity):
    pass


class IfcQuantityTime(IfcPhysicalSimpleQuantity):
    pass


class IfcQuantityVolume(IfcPhysicalSimpleQuantity):
    pass


class IfcQuantityWeight(IfcPhysicalSimpleQuantity):
    pass


class IfcPersonAndOrganization(entity_instance):
    pass


class IfcPerson(entity_instance):
    pass


class IfcOwnerHistory(entity_instance):
    pass


class IfcOrganization(entity_instance):
    pass


class IfcObjectPlacement(entity_instance):
    pass


class IfcGridPlacement(IfcObjectPlacement):
    pass


class IfcLinearPlacement(IfcObjectPlacement):
    pass


class IfcLocalPlacement(IfcObjectPlacement):
    pass


class IfcNamedUnit(entity_instance):
    pass


class IfcContextDependentUnit(IfcNamedUnit):
    pass


class IfcConversionBasedUnit(IfcNamedUnit):
    pass


class IfcConversionBasedUnitWithOffset(IfcConversionBasedUnit):
    pass


class IfcSIUnit(IfcNamedUnit):
    pass


class IfcMonetaryUnit(entity_instance):
    pass


class IfcMeasureWithUnit(entity_instance):
    pass


class IfcMaterialUsageDefinition(entity_instance):
    pass


class IfcMaterialLayerSetUsage(IfcMaterialUsageDefinition):
    pass


class IfcMaterialProfileSetUsage(IfcMaterialUsageDefinition):
    pass


class IfcMaterialProfileSetUsageTapering(IfcMaterialProfileSetUsage):
    pass


class IfcMaterialList(entity_instance):
    pass


class IfcMaterialDefinition(entity_instance):
    pass


class IfcMaterial(IfcMaterialDefinition):
    pass


class IfcMaterialConstituent(IfcMaterialDefinition):
    pass


class IfcMaterialConstituentSet(IfcMaterialDefinition):
    pass


class IfcMaterialLayer(IfcMaterialDefinition):
    pass


class IfcMaterialLayerWithOffsets(IfcMaterialLayer):
    pass


class IfcMaterialLayerSet(IfcMaterialDefinition):
    pass


class IfcMaterialProfile(IfcMaterialDefinition):
    pass


class IfcMaterialProfileWithOffsets(IfcMaterialProfile):
    pass


class IfcMaterialProfileSet(IfcMaterialDefinition):
    pass


class IfcMaterialClassificationRelationship(entity_instance):
    pass


class IfcLightIntensityDistribution(entity_instance):
    pass


class IfcLightDistributionData(entity_instance):
    pass


class IfcIrregularTimeSeriesValue(entity_instance):
    pass


class IfcGridAxis(entity_instance):
    pass


class IfcExternalReference(entity_instance):
    pass


class IfcClassificationReference(IfcExternalReference):
    pass


class IfcDocumentReference(IfcExternalReference):
    pass


class IfcExternallyDefinedHatchStyle(IfcExternalReference):
    pass


class IfcExternallyDefinedSurfaceStyle(IfcExternalReference):
    pass


class IfcExternallyDefinedTextFont(IfcExternalReference):
    pass


class IfcLibraryReference(IfcExternalReference):
    pass


class IfcExternalInformation(entity_instance):
    pass


class IfcClassification(IfcExternalInformation):
    pass


class IfcDocumentInformation(IfcExternalInformation):
    pass


class IfcLibraryInformation(IfcExternalInformation):
    pass


class IfcDimensionalExponents(entity_instance):
    pass


class IfcDerivedUnitElement(entity_instance):
    pass


class IfcDerivedUnit(entity_instance):
    pass


class IfcCoordinateReferenceSystem(entity_instance):
    pass


class IfcProjectedCRS(IfcCoordinateReferenceSystem):
    pass


class IfcCoordinateOperation(entity_instance):
    pass


class IfcMapConversion(IfcCoordinateOperation):
    pass


class IfcConstraint(entity_instance):
    pass


class IfcMetric(IfcConstraint):
    pass


class IfcObjective(IfcConstraint):
    pass


class IfcConnectionGeometry(entity_instance):
    pass


class IfcConnectionCurveGeometry(IfcConnectionGeometry):
    pass


class IfcConnectionPointGeometry(IfcConnectionGeometry):
    pass


class IfcConnectionPointEccentricity(IfcConnectionPointGeometry):
    pass


class IfcConnectionSurfaceGeometry(IfcConnectionGeometry):
    pass


class IfcConnectionVolumeGeometry(IfcConnectionGeometry):
    pass


class IfcBoundaryCondition(entity_instance):
    pass


class IfcBoundaryEdgeCondition(IfcBoundaryCondition):
    pass


class IfcBoundaryFaceCondition(IfcBoundaryCondition):
    pass


class IfcBoundaryNodeCondition(IfcBoundaryCondition):
    pass


class IfcBoundaryNodeConditionWarping(IfcBoundaryNodeCondition):
    pass


class IfcApproval(entity_instance):
    pass


class IfcAppliedValue(entity_instance):
    pass


class IfcCostValue(IfcAppliedValue):
    pass


class IfcApplication(entity_instance):
    pass


class IfcAddress(entity_instance):
    pass


class IfcPostalAddress(IfcAddress):
    pass


class IfcTelecomAddress(IfcAddress):
    pass


class IfcActorRole(entity_instance):
    pass


